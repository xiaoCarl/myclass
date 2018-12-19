# 文件说明

1. game.py :定义了 棋盘board类和game类， game类有一个棋盘board类的实例

2. human_play.py 定义了human类， 定义了 human vs AI的主函数(入口函数)run()

3. train.py 定义了AI自训练的TrainPipeline类。 AI自训练TrainPipeline().run()

notic： move = player.get_action(board) : 这是AI 或者human的获取下一步位置的接口，human player还是mstc_player或者ai_player 都会定义该函数。

------------------------------------------------------------------------------------------

4. mcts_pure.py :  纯mcts算法的AI
5. mcts_alphaZero.py： 基于训练数据的AI

------------------------------------------------------------------------------------------
6. policy_value_net_tesorfolow.py : 基于tesorflow框架的算法
7. policy_value_net_numpy.py : 基于numpy模块搭建的算法
8. policy_value_net_keras.py : 基于Keras框架的算法
9. policy_value_net_pytorch.py: 基于PyTorch框架的算法
10. policy_value_net.py : 基于Theano and Lasagne框架的算法
