from board import Board
from player import Human
from expert import ExpertPlayer
import logging

def log_config():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(filename = 'gomoku.log', 
                        level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT)

def run():
    
    log_config()

    my_board = Board()
    play1 = ExpertPlayer()
    play2 = Human()

    my_board.start(play1, play2) 


if __name__ == '__main__':
    run()
