# gra
import random
def main():
    # Define an empty rocklist to append rocks to, define random integers, call functions
    board = [1,2,3,4,5]
    name1, name2 = get_players()

    player = name1  # Set current player to 1 (for switching later)

    get_board(board,  player)  # Set initial board

    play_again(board, name1, name2, player)


# Post: takes no arguments and returns the player names as strings entered by the user
def get_players():
    return input("Enter player 1 name: "), input("Enter player 2 name: ")



def get_board(board,  player):
    # Get initial board
    print("Let's look at the board now.")
    print("-" * 25)
    for i in range(len(board)):
        rocks = board[i]
        print('Pile {}: {}'.format(i + 1, 'O' * rocks))
    print("-" * 25)



def get_valid_input(board, player):
    # Begin loop that tests for valid input - if valid, break loop - if not, keep asking
    while True:
        piles = input(' {}, Pick a pile to remove from: '.format(player))
        stones = input('{}, how many stones to remove? ')

        # If all condiitons for input are CORRECT, break out of loop
        if (stones and piles) and (stones.isdigit()) and (piles.isdigit()):
            if (int(stones) > 0) and (int(piles) <= len(board)) and (int(piles) > 0):
                if (int(stones) <= board[int(piles) - 1]):
                    if (int(stones) != 0) and (int(piles) != 0):
                        break

        # If not, display this statement
        print("Hmmm. You entered an invalid value. Try again, {}.".format(player))

    # Update state
    board[int(piles) - 1] -= int(stones)

    # Keep playing game
    continue_game(board, player)


def continue_game(board, player):
    print("Let's look at the board now.")
    print("-" * 25)
    for i in range(len(board)):
        print("Pile {}: {}".format(i + 1, 'O' * board[i]))

    print("-" * 25)

    # In the case when game is over, do not display computer hint for empty board
    # if rockList != [0] * len(rockList):
    #     nim_sum(rockList, randPile)

    # print(rockList)


def play_again(board, name1, name2, player):
    # Begin loop to initiate player switching
    while True:
        get_valid_input(board, player)

        # To determine winner, check if rockList contains all 0's on that player's turn
        if sum(board) == 1:
            print("{} is the winner of this round!".format(name2 if player == name1 else name1))
            break
        #     user = input("Do you want to play again? Enter y for yes, anything for no: ")
        #
        #     if user.lower() == 'y':
        #         # reset all conditions, start the game again
        #         rockList = []
        #         randPile = random.randint(2, 5)
        #         name1, name2 = get_players()
        #         player = name1
        #         get_board(rockList, randPile, randRock, player)
        #         get_valid_input(rockList, randPile, player)
        #
        #     else:
        #         break
        #
        # switch players 2->1, 1->2
        if player == name1:
            player = name2

        else:
            player = name1




main()

#uzytkownicy ai