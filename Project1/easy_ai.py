# gra
from easyAI import TwoPlayerGame, Negamax, AI_Player
import random


class Nim(TwoPlayerGame):

    def __init__(self, players=None, piles=(1, 2, 3, 4, 5)):
        self.players = players
        self.piles = list(piles)
        self.current_player = 1  # player 1 starts.

    def possible_moves(self):
        return [
            "%d,%d" % (i + 1, j)
            for i in range(len(self.piles))
            for j in range(1, self.piles[i]+1)
        ]

    def make_move(self, move):
        move = list(map(int, move.split(",")))

        # 10% chance to reduce move[1] by 1
        if random.random() < 0.1 and move[1] > 0:
            move[1] -= 1

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

def play_ai_vs_ai(num_games=10):
    ai_algo = Negamax(3)  # Set search depth
    results = {"AI1": 0, "AI2": 0}

    for game_num in range(num_games):
        # Switch starting player every game
        players = [AI_Player(ai_algo), AI_Player(ai_algo)] if game_num % 2 == 0 else [AI_Player(ai_algo), AI_Player(ai_algo)][::-1]
        game = Nim(players)
        game.play()

        winner = "AI1" if game.current_player == 2 else "AI2"
        results[winner] += 1
        print(f"Game {game_num + 1}: {winner} wins!")

    print("\nFinal Results:")
    print(f"AI1 Wins: {results['AI1']}")
    print(f"AI2 Wins: {results['AI2']}")


if __name__ == "__main__":
    play_ai_vs_ai(10)  # Run 10 AI vs AI games
