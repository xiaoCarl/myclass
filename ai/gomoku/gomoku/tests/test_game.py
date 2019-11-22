import unittest

from gomoku import game

class TestGame(unittest.TestCase):
    def setUp(self):        
        pass

    def test_board_move_to_location(self):
        self.board = game.Board(width=3, height=3, n_in_row=2)
        h,w = self.board.move_to_location(5)
        self.assertEqual(h,1,"move to location error!")
        self.assertEqual(w,3,"move to location error!")
