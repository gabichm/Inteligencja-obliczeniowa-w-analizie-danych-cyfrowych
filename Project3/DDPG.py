
import copy
import numpy as np
from keras import layers,models,optimizers
from keras import backend as K
import tensorflow as tf
from keras import regularizers, initializers



class Actor():
    """Actor (Policy) Model"""

    def __init__(self,state_size,action_size,action_low,action_high):
        """Initialize and build actor model
        
        Params:
        ======
            state_size(int): size of the observation space
            action_size(int): size of the action space
            action_low(array): min value of each action dimension
            action_high(array): max value of each action dimension
        """

        self.state_size = state_size
        self.action_size = action_size
        self.action_high = action_high
        self.action_low = action_low
        self.action_range = self.action_high-self.action_low

        # Build actor model
        self.build_model()

    def build_model(self):
        """Return an actor policy network which maps states to actions"""

        # Define input layers
        states = layers.Input(shape=(self.state_size,),name='states')

        # Define hidden layers

        net = layers.Dense(units=400,kernel_regularizer=regularizers.l2(1e-6))(states)
        net = layers.BatchNormalization()(net)
        net = layers.Activation("relu")(net)
        net = layers.Dense(units=300,kernel_regularizer=regularizers.l2(1e-6))(net)
        net = layers.BatchNormalization()(net)
        net = layers.Activation("relu")(net)

        # Define output layers
        raw_actions = layers.Dense(units=self.action_size,activation='sigmoid',
            name='raw_actions',kernel_initializer=initializers.RandomUniform(minval=-0.003, maxval=0.003))(net)

        # Scale raw actions to action space range

        actions = layers.Lambda(lambda x: (x*self.action_range)+self.action_low,
            name='actions')(raw_actions)

        # Create Keras model

        self.model = models.Model(inputs=states,outputs=actions)

        # Define loss function using action value (Q value) gradients

        action_gradients = layers.Input(shape=(self.action_size,))
        loss = tf.reduce_mean(tf.reduce_sum(-action_gradients * actions, axis=1))

        # Define optimizers
        optimizer = optimizers.Adam(lr = 0.0001)
        updates_op = optimizer.get_updates(params=self.model.trainable_weights, loss=loss)

        
        self.train_fn = K.function(
            inputs=[self.model.input, action_gradients, K.learning_phase()],
            outputs=[],
            updates=updates_op)




class Critic():
    """Critic model Q(s,a)"""

    def __init__(self,state_size,action_size):
        """Initialize model
        
        Params:
        =======
            state_size(int): dimension of observation space
            action_size(int): dimension of action space
        """

        self.state_size = state_size
        self.action_size = action_size

        self.build_model()

    def build_model(self):
        """Build a critic (value) network that maps (state, action) pairs -> Q-values."""
        # Define input layers
        states = layers.Input(shape=(self.state_size,), name='states')
        actions = layers.Input(shape=(self.action_size,), name='actions')

        # Add hidden layer(s) for state pathway
        net_states = layers.Dense(units=400,kernel_regularizer=regularizers.l2(1e-6))(states)
        net_states = layers.BatchNormalization()(net_states)
        net_states = layers.Activation("relu")(net_states)

        net_states = layers.Dense(units=300, kernel_regularizer=regularizers.l2(1e-6))(net_states)

        # Add hidden layer(s) for action pathway
        net_actions = layers.Dense(units=400,kernel_regularizer= regularizers.l2(1e-6))(actions)
        net_actions = layers.Dense(units=300,kernel_regularizer= regularizers.l2(1e-6))(net_actions)
        # Combine state and action pathways
        net = layers.Add()([net_states, net_actions])
        net = layers.Activation('relu')(net)

        # Add final output layer to prduce action values (Q values)
        Q_values = layers.Dense(units=1, name='q_values',kernel_regularizer= regularizers.l2(0.01),
        kernel_initializer= initializers.RandomUniform(minval=-0.003, maxval=0.003))(net)

        # Create Keras model
        self.model = models.Model(inputs=[states, actions], outputs=Q_values)

        # Define optimizer and compile model for training with built-in loss function
        optimizer = optimizers.Adam(lr=0.001)
        self.model.compile(optimizer=optimizer, loss='mse')

        # Compute action gradients (derivative of Q values w.r.t. to actions)
        action_gradients = K.gradients(Q_values, actions)

        # Define an additional function to fetch action gradients (to be used by actor model)
        self.get_action_gradients = K.function(
            inputs=[*self.model.input, K.learning_phase()],
            outputs=action_gradients)
        


class OUNoise:
    """Ornstein-Uhlenbeck process."""

    def __init__(self, size, mu, theta, sigma):
        """Initialize parameters and noise process."""
        self.mu = mu * np.ones(size)
        self.theta = theta
        self.sigma = sigma
        self.reset()

    def reset(self):
        """Reset the internal state (= noise) to mean (mu)."""
        self.state = copy.copy(self.mu)

    def sample(self):
        """Update internal state and return it as a noise sample."""
        x = self.state
        dx = self.theta * (self.mu - x) + self.sigma * np.random.randn(len(x))
        self.state = x + dx
        return self.state

class DDPGAgent():
    """Reinforcement learning agent who learns using DDPG"""

    def __init__(self,task):
        """Initialize models"""
        self.env = task
        self.state_size = task.observation_space.shape[0]
        self.action_size = task.action_space.shape[0]
        self.action_high = task.action_space.high
        self.action_low = task.action_space.low
        

        # Initialize Actor (policy) models
        self.actor_local = Actor(self.state_size,self.action_size,self.action_low,self.action_high)
        self.actor_target = Actor(self.state_size,self.action_size,self.action_low,self.action_high)

        # Initialize Critic (value) models
        self.critic_local = Critic(self.state_size,self.action_size)
        self.critic_target = Critic(self.state_size,self.action_size)

        # Initialize target model parameters with local model parameters
        self.actor_target.model.set_weights(self.actor_local.model.get_weights())
        self.critic_target.model.set_weights(self.critic_local.model.get_weights())

        # Noise process
        self.exploration_mu = 0
        self.exploration_theta = 0.15
        self.exploration_sigma = 0.2
        self.noise = OUNoise(self.action_size, self.exploration_mu, self.exploration_theta, self.exploration_sigma)

        # Replay buffer

        self.buffer_size = 100000 
        self.batch_size = 64
        self.memory = ReplayBuffer(self.buffer_size,self.batch_size)

         # Algorithm parameters
        self.gamma = 0.99  # discount factor
        self.tau = 0.001  # for soft update of target parameters

    def reset_episode(self,task):
        """Return state after reseting task"""
        self.noise.reset()
        state = task.reset()
        self.last_state = state
        return state

    def step(self,action,reward,next_state,done):
        # Add experience to memory
        self.memory.add_experience(self.last_state,action,reward,next_state,done)

        # Learn is memory is larger than batch size
        if len(self.memory) > self.batch_size:
            experiences = self.memory.sample()
            self.learn(experiences)
        
        # Roll over state
        self.last_state = next_state

    def act(self,state):
        """Returns action using the policy network """
        state = np.reshape(state,[-1,self.state_size])
        action = self.actor_local.model.predict(state)[0]
        return list(action+self.noise.sample())

    def learn(self,experiences):
        # Convert experience tuples to separate arrays for each element

        states = np.vstack([e.state for e in experiences if e is not None]).astype(np.float32).reshape(-1,self.state_size)
        actions = np.array([e.action for e in experiences if e is not None]).astype(np.float32).reshape(-1,self.action_size) 
        next_states = np.vstack([e.next_state for e in experiences if e is not None]).astype(np.float32).reshape(-1,self.state_size)
        rewards = np.array([e.reward for e in experiences if e is not None]).astype(np.float32).reshape(-1,1)
        dones = np.array([e.done for e in experiences if e is not None]).astype(np.uint8).reshape(-1,1)

        # Get predicted next-state actions and Q values from target models
        #     Q_targets_next = critic_target(next_state, actor_target(next_state))
        actions_next = self.actor_target.model.predict(next_states)
        Q_targets_next = self.critic_target.model.predict([next_states,actions_next])

        # Compute Q targets for current states and train critic model (local)
        Q_targets = rewards + self.gamma*Q_targets_next*(1-dones)
        self.critic_local.model.train_on_batch(x=[states,actions],y=Q_targets)
        # Train actor model (local)
        action_gradients = np.reshape(self.critic_local.get_action_gradients([states,actions,0]),
        [-1,self.action_size])
        self.actor_local.train_fn([states,action_gradients,1])

        # Soft-update target models
        self.soft_update(self.actor_local.model,self.actor_target.model)
        self.soft_update(self.critic_local.model,self.critic_target.model)

    def soft_update(self,local_model,target_model):
        local_weights = np.array(local_model.get_weights())
        target_weights = np.array(target_model.get_weights())
        assert len(local_weights) == len(target_weights), "Local and target model parameters must have the same size"

        new_weights = self.tau*local_weights + (1-self.tau)*target_weights
        target_model.set_weights(new_weights)

    def save_model(self,path):
        self.actor_local.model.save_weights(path)

    def load_model(self,path):
        self.actor_local.model.load_weights(path)

    def act_only(self,state):
        state = np.reshape(state,[-1,self.state_size])
        action = self.actor_local.model.predict(state)[0]
        return list(action)

        


    