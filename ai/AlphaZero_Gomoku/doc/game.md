
# Board类
## 属性

width  : int  棋盘的宽度  
height : int  棋盘的高度

states  :{}     棋盘的状态，定义为一个字典
        states[key] = value;
        key  :是所有棋盘的位置，总共为width*height
        value:该位置上下的棋，为player1 还是player2


players :[1,2] ; 分别代表player1或者player2
n_in_row: int; 表示多少个子连在一起赢，=5 表示是5子棋，=3表示3子棋
current_player: int;  1 (player1) 或者 2(player2),  当前走棋方，初始为player1

availables:[];存储目前所有可以走棋的位置， 一个列表,列表的大小为width*height
last_move : int ,范围：0到width*height-1  最后一步棋

## 方法
1. init_board(self,start_player=0) :棋盘初始化
2. move_to_location(self, move) :将move转换为棋盘上的位置。一个棋盘move按照编号0 - width*height -1 个,  将这个值转换为棋盘的具体的w, h
    3*3 board's moves like:
        6 7 8
        3 4 5
        0 1 2
    and move 5's location is (1,2)
3. location_to_move(self, location) :将二维表示的位置转换为一维的move值, move_to_location函数的逆运算这两个方法，就是简化棋盘的定义，用一个一维的move，代表二维的位置，这些我记录棋盘状态的时候，就不需要定义一个三维的结构，只需要一个二维的结构
4. current_state(self) : 返回棋盘的局面，通过4个width*height数组 描述棋盘的局面信息，具体参见后面的描述：
    square_state[0]  数组表示player1(AI)下的move位置
    square_state[1]  数组表示payer2(对手)下的move位置
    square_state[2]  数组表示最后一步下的move位置
    square_state[3]  数组表示下一步是player1(全0)，还是player2(全1)
5. do_move(self, move) : 每做一步，相关棋盘信息的更新

6. has_a_winner(self) : 判断这盘棋是否已经达到胜利状态，5个连在一起，注意，需要考虑二维空间里面5个连在一起的子，展开后在一维空间的分布

7. game_end(self): 判断棋是胜，负，还是和
8. get_current_player(self) : 获取当前下棋方


--------------------------------------------------------------------------------------
# game类

