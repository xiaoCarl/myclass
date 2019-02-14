from __future__ import print_function

from board import Board
from mcts import  MonteCarlo

class Player(object):
    def get_action(self,board):
        '''
        Get player next action.
        Return: the next action.
        '''
        return action

class MCTS_Player(Player):
    def __init__(self):
        self.mcts  = MonteCarlo()

    def get_action(self,board):
        action = 2
        return action


class Human(Player):
    def __init__(self):
        pass

    def get_action(self,board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            action = self.location_to_action(board, location)
        except Exception as e:
            action = -1
        if action == -1 or action not in board.availables:
            print("invalid move")
            action = self.get_action(board)
        return action

    def location_to_action(self, board, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        action = h * board.width + w
        if action not in range(board.width * board.height):
            return -1
        return action
   


def run():
    my_board = Board()

    play1 = Human()
    play2 = Human()
    #m_mcst = MonteCarlo()
    my_board.start(play1, play2)


if __name__ == '__main__':
    run()