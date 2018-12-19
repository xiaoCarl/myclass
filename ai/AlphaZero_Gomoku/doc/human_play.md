# human类

## 属性
player： 存储在board.players对应 human的索引

## 方法
set_player_ind(self, p) : 设置human的在board.players中的索引
get_action(self, board) :获取下一步位置

-----------------------------------------------------------------------
# AI vi Human的主函数run
1. 初始化board实例
2. 初始化game实例

3. 对加载训练的神经网络数据
4. 用这个数据，初始化AI player

5. 初始化human player
6. 开始比赛game.start_game()