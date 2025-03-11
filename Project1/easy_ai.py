import random
import time
import easyAI

LOWERBOUND, EXACT, UPPERBOUND = -1, 0, 1

inf = float("infinity")

def negamax_no_alfa_beta(game, depth, origDepth, scoring, tt=None):
    """
    This implements a basic Negamax algorithm without alpha-beta pruning or transposition tables.
    """

    lookup = None if (tt is None) else tt.lookup(game)

    if lookup is not None:
        if lookup["depth"] >= depth:
            flag, value = lookup["flag"], lookup["value"]
            if flag == EXACT:
                if depth == origDepth:
                    game.ai_move = lookup["move"]
                return value

    if (depth == 0) or game.is_over():
        return scoring(game) * (1 + 0.001 * depth)

    if lookup is not None:
        possible_moves = game.possible_moves()
        possible_moves.remove(lookup["move"])
        possible_moves = [lookup["move"]] + possible_moves
    else:
        possible_moves = game.possible_moves()

    state = game
    best_move = possible_moves[0]
    if depth == origDepth:
        state.ai_move = possible_moves[0]

    bestValue = -inf
    unmake_move = hasattr(state, "unmake_move")

    for move in possible_moves:
        if not unmake_move:
            game = state.copy()  

        game.make_move(move)
        game.switch_player()

        move_value = -negamax_no_alfa_beta(game, depth - 1, origDepth, scoring, tt)

        if unmake_move:
            game.switch_player()
            game.unmake_move(move)

        if bestValue < move_value:
            bestValue = move_value
            best_move = move

    if tt is not None:
        assert best_move in possible_moves
        tt.store(
            game=state,
            depth=depth,
            value=bestValue,
            move=best_move,
            flag=EXACT,  
        )

    return bestValue

class NegamaxNoAlfaBeta:
    """
    This implements the basic Negamax algorithm without alpha-beta pruning. 
    The AI simply looks at all possible moves and picks the one with the best outcome.
    """

    def __init__(self, depth, scoring=None, win_score=+inf, tt=None):
        self.scoring = scoring
        self.depth = depth
        self.tt = tt
        self.win_score = win_score

    def __call__(self, game):
        """
        Returns the AI's best move given the current state of the game.
        """

        scoring = (
            self.scoring if self.scoring else (lambda g: g.scoring())
        )  # horrible hack

        self.alpha = negamax_no_alfa_beta(
            game,
            self.depth,
            self.depth,
            scoring,
            self.tt,
        )
        return game.ai_move


def expecti_minmax(game, depth, origDepth, scoring, is_max_player, alpha=-inf, beta=inf, tt=None):
    """
    Implements Expecti-Minimax with alpha-beta pruning.
    """
    alphaOrig = alpha

    lookup = None if (tt is None) else tt.lookup(game)

    if lookup is not None:
        if lookup["depth"] >= depth:
            flag, value = lookup["flag"], lookup["value"]
            if flag == EXACT:
                if depth == origDepth:
                    game.ai_move = lookup["move"]
                return value
            elif flag == LOWERBOUND:
                alpha = max(alpha, value)
            elif flag == UPPERBOUND:
                beta = min(beta, value)

            if alpha >= beta:
                if depth == origDepth:
                    game.ai_move = lookup["move"]
                return value

    if depth == 0 or game.is_over():
        return scoring(game) * (1 + 0.001 * depth)

    if lookup is not None:
        possible_moves = game.possible_moves()
        possible_moves.remove(lookup["move"])
        possible_moves = [lookup["move"]] + possible_moves
    else:
        possible_moves = game.possible_moves()

    state = game
    best_move = possible_moves[0]
    if depth == origDepth:
        state.ai_move = possible_moves[0]

    bestValue = -inf
    unmake_move = hasattr(state, "unmake_move")

    if is_max_player:
        # Max player
        for move in possible_moves:
            if not unmake_move:
                game = state.copy()

            game.make_move(move)
            game.switch_player()

            move_value = -expecti_minmax(game, depth - 1, origDepth, scoring, not is_max_player, -beta, -alpha, tt)

            if unmake_move:
                game.switch_player()
                game.unmake_move(move)

            if bestValue < move_value:
                bestValue = move_value
                best_move = move

            alpha = max(alpha, bestValue)

            if alpha >= beta:
                break
    else:
        expected_value = 0
        total_probability = 0
        for move in possible_moves:
            if not unmake_move:
                game = state.copy()

            game.make_move(move)
            game.switch_player()

            move_value = expecti_minmax(game, depth - 1, origDepth, scoring, not is_max_player, alpha, beta, tt)

            if unmake_move:
                game.switch_player()
                game.unmake_move(move)

            total_probability += 1
            expected_value += move_value

        expected_value /= total_probability
        bestValue = expected_value

    if tt is not None:
        assert best_move in possible_moves
        tt.store(
            game=state,
            depth=depth,
            value=bestValue,
            move=best_move,
            flag=EXACT
            if bestValue > alphaOrig
            else (LOWERBOUND if bestValue <= alpha else UPPERBOUND),
        )

    return bestValue


class ExpectiMinimax:
    """
    Implements Expecti-Minimax with alpha-beta pruning. The AI can handle both max and chance players.
    """

    def __init__(self, depth, scoring=None, win_score=+inf, tt=None):
        self.scoring = scoring
        self.depth = depth
        self.tt = tt
        self.win_score = win_score

    def __call__(self, game):
        """
        Returns the AI's best move given the current state of the game.
        """

        scoring = (
            self.scoring if self.scoring else (lambda g: g.scoring())
        )

        self.alpha = expecti_minmax(
            game,
            self.depth,
            self.depth,
            scoring,
            is_max_player=True,  # Starting as max player
            alpha=-self.win_score,
            beta=self.win_score,
            tt=self.tt,
        )
        return game.ai_move


class Nim(easyAI.TwoPlayerGame):
    def __init__(self, players=None, piles=(1, 2, 3, 4, 5), prob=False):
        self.players = players
        self.piles = list(piles)
        self.current_player = 1  # player 1 starts.
        self.prob = prob
        self.history = []

    def possible_moves(self):
        return [
            "%d,%d" % (i + 1, j)
            for i in range(len(self.piles))
            for j in range(1, self.piles[i]+1)
        ]

    def make_move(self, move):
        move = list(map(int, move.split(",")))
        if self.prob and random.random() < 0.1 and move[1] > 0:
            move[1] -= 1  # 10% chance to have a move smaller than intended
        self.piles[move[0] - 1] -= move[1]

    def show(self):
        print(" ".join(map(str, self.piles)))

    def win(self):
        if sum(self.piles) == 0:
            return True

    def is_over(self):
        return self.win()

    def scoring(self):
        return 100 if self.win() else 0


def time_count(ai_algo, prob=False, num_games=10):
    results = {"AI1": 0, "AI2": 0, "time_AI1": 0, "time_AI2": 0, "moves_AI1": 0, "moves_AI2": 0}

    for game_num in range(num_games):
        players = [easyAI.AI_Player(ai_algo), easyAI.AI_Player(ai_algo)] if game_num % 2 == 0 else [easyAI.AI_Player(ai_algo), easyAI.AI_Player(ai_algo)][::-1]
        game = Nim(players, prob=prob)

        while not game.is_over():
            start_time = time.time()
            game.play_move(game.get_move())
            full_time = time.time() - start_time

            if game.current_player == 2:
                results["time_AI1"] += full_time
                results["moves_AI1"] += 1
            else:
                results["time_AI2"] += full_time
                results["moves_AI2"] += 1

        winner = "AI1" if game.current_player == 2 else "AI2"
        results[winner] += 1

    results["avg_time_AI1"] = results["time_AI1"] / results["moves_AI1"] if results["moves_AI1"] else 0
    results["avg_time_AI2"] = results["time_AI2"] / results["moves_AI2"] if results["moves_AI2"] else 0
    return results


def compare_algorithms():
    algorithms = {
        "Negamax ": easyAI.Negamax(6),
        "Negamax without Alpha-Beta ": NegamaxNoAlfaBeta(6),
        "Expecti-minmax with Alpha-Beta": ExpectiMinimax(6)
    }

    for name, algo in algorithms.items():
        print(f"Testing {name} (Deterministic)")
        deterministic_results = time_count(algo, prob=False)
        print(deterministic_results)

        print(f"Testing {name} (Probabilistic)")
        probabilistic_results = time_count(algo, prob=True)
        print(probabilistic_results)


if __name__ == "__main__":
    compare_algorithms()  # Run 10 AI vs AI games
