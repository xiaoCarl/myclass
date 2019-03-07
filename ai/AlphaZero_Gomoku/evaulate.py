from collections import defaultdict, deque
from expert import ExpertPlayer
from game import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure
from mcts_alphaZero import MCTSPlayer


def evaluate_player(player1,player2,n_games=10):
    """
    Evaluate the trained policy by playing against the pure MCTS player
    Note: this is only for monitoring the progress of training
    current_mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
                                     c_puct=self.c_puct,
                                     n_playout=self.n_playout)
    """

    board = Board(width=9, height=9, n_in_row=5)
    game = Game(board)
        
    win_cnt = defaultdict(int)
    for i in range(n_games):
        winner = game.start_play(player1,player2,
                                 start_player=i % 2,
                                 is_shown=0)
        print(winner)
        win_cnt[winner] += 1
    win_ratio = 1.0*(win_cnt[1] + 0.5*win_cnt[-1]) / n_games
    print("player1:{}vs player2:{}. result: win: {}, lose: {}, tie:{}".format(
            player1,player2, win_cnt[1], win_cnt[2], win_cnt[-1]))
    return win_ratio

if __name__ == '__main__':

    player1 = MCTS_Pure(c_puct=5, n_playout=1000)
    player2 = ExpertPlayer()

    win_ration = evaluate_player(player1,player2,n_games=10)
