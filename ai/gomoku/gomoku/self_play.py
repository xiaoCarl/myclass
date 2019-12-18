import numpy as np

def get_board_state(board):
    """
    输入：当前棋盘，输出：棋盘训练的state格式:4*width*height
    """
    square_state = np.zeros((4, board.width, board.height))
    if board.states:
        moves, players = np.array(list(zip(*board.states.items())))
        move_curr = moves[players == board.current_player]
        move_oppo = moves[players != board.current_player]
        square_state[0][move_curr // board.width,
                        move_curr % board.height] = 1.0
        square_state[1][move_oppo // board.width,
                        move_oppo % board.height] = 1.0
        # indicate the last move location
        square_state[2][board.last_move // board.width,
                        board.last_move % board.height] = 1.0
    if len(board.states) % 2 == 0:
        square_state[3][:, :] = 1.0  # indicate the colour to play
    return square_state[:, ::-1, :]


def start_self_play(board, player):
    """
    输入:棋盘，自对弈的player
    输出：下完一盘棋后，完整的对弈数据集，打包格式zip(states,probs,value)
    """
    board.init_board()
    p1, p2 = board.players
    states, probs, current_players = [], [], []
    while True:
        move, move_probs = player.get_action(board,return_prob=1)
        # store the data
        states.append(get_board_state(board))
        probs.append(move_probs)
        current_players.append(board.current_player)
        # perform a move
        board.do_move(move)
            
        end, winner = board.game_end()
        if end:
        # winner from the perspective of the current player of each state
            value = np.zeros(len(current_players))

            if winner != -1:
                value[np.array(current_players) == winner] = 1
                value[np.array(current_players) != winner] =-1

                # reset MCTS root node
            player.reset_player()
            return winner, zip(states, probs, value)


