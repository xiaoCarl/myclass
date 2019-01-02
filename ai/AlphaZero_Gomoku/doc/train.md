# TrainPipeline类

## 属性
1.  训练的棋盘信息
    self.board_width = 6
    self.board_height = 6
    self.n_in_row = 4
    self.board = Board(width=self.board_width,
                       height=self.board_height,
                       n_in_row=self.n_in_row)
    self.game = Game(self.board)

2.  training params 训练参数
    self.learn_rate = 2e-3
    self.lr_multiplier = 1.0  # adaptively adjust the learning rate based on KL
    self.temp = 1.0  # the temperature param
    self.n_playout = 400  # num of simulations for each move
    self.c_puct = 5
    self.buffer_size = 10000
    self.batch_size = 512  # mini-batch size for training
    self.data_buffer = deque(maxlen=self.buffer_size)
    self.play_batch_size = 1
    self.epochs = 5  # num of train_steps for each update
    self.kl_targ = 0.02
    self.check_freq = 50
    self.game_batch_num = 1500
    self.best_win_ratio = 0.0
    
    # num of simulations used for the pure mcts, which is used as
    # the opponent to evaluate the trained policy
    self.pure_mcts_playout_num = 1000
