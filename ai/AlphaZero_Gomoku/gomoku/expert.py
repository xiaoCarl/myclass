# encoding: utf-8
from player import Player,Human
from board import Board

from collections import defaultdict
import logging


def log_config():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(filename = 'gomoku.log', 
                        level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT)



class Expert(object):
    def __init__(self):
        self.height = 12
        self.width  = 12
        self.grade  = 100
        self.max_value = 1008611
        self.move_value=defaultdict(lambda:0)

    def location_to_move(self,i,j):
        """location = (i,j),move=i+j*width 
        """
        return i+j*self.width

    def move_to_location(self,move):
        """location = (i,j),dot=i+j*width 
        """
        i = move % self.width
        j = move // self.height
        return [i, j]

    def get_loc_player(self, i, j):
        move = self.location_to_move(i,j)
        return self.board.states[move]

    def scan_updown(self,i,j,player):
        value = 0
        count = 0      #统计连续本方旗子或者空棋的个数
        grade = self.grade

        m, n = i, j-1  #向上移动一步
        while n >= 0 :
            is_continue,value,grade =self.caculate_once_value(m,n,player,value,grade)
            if is_continue: 
                n = n-1 
            else:
                break #向上移动一步  
            count +=1 

        grade = self.grade  #换一个方向，权值调回初始值
        n = j + 1       
        while n < self.board.height :
            is_continue,value,grade =self.caculate_once_value(m,n,player,value,grade)
            if is_continue:
                n = n + 1
            else:
                break #向下移动一步  
            count +=1 

        return value if count >= 4 else 0  #如果这个方向可成5子，就返回alue，否则就是0

    def scan_leftright(self,i,j,player):
        value = 0
        count = 0      #统计连续本方旗子或者空棋的个数
        grade = self.grade

        m, n = i-1, j  #向左移动一步
        while m >= 0 :
            is_continue,value,grade =self.caculate_once_value(m,n,player,value,grade)
            if is_continue:
                m = m-1
            else:
                break #向左移动一步  
            count +=1 

        grade = self.grade  #换一个方向，权值调回初始值
        m = i + 1   #向右      
        while m < self.board.width:
            is_continue,value,grade =self.caculate_once_value(m,n,player,value,grade)
            if is_continue:
                m = m + 1
            else:
                break #向右移动一步  
            count +=1 

        return value if count >= 4 else 0  #如果这个方向可成5子，就返回alue，否则就是0

    def scan_left_updown(self,i,j,player):
        value = 0
        count = 0      #统计连续本方旗子或者空棋的个数

        grade = self.grade
        m, n = i-1, j-1        #向左上移动一步
        while m >= 0 and n >=0:
            is_continue,value,grade =self.caculate_once_value(m,n,player,value,grade)
            if is_continue:
                m, n = m-1, n-1
            else:
                break  #向左上继续移动一步     
            count +=1 

        grade=self.grade
        m, n = i+1, j+1   #向左下      
        while m < self.width and n < self.height:
            is_continue,value,grade =self.caculate_once_value(m,n,player,value,grade)
            if is_continue:
                m, n = m+1, n+1
            else:
                break  #向左下继续移动一步     
            count +=1 

        return value if count >= 4 else 0  #如果这个方向可成5子，就返回alue，否则就是0

    def scan_right_updown(self,i,j,player):
        value = 0
        count = 0         #统计连续本方旗子或者空棋的个数

        grade = self.grade
        m, n = i+1, j-1   #向右上移动一步
        while m < self.width and n >=0:
            is_continue,value,grade =self.caculate_once_value(m,n,player,value,grade)
            if is_continue:
                m, n = m+1, n-1
            else:
                break  #向右上继续移动一步     
            count +=1 

        grade=self.grade
        m, n = i-1, j+1   #向右下      
        while m >=0 and n < self.height:
            is_continue,value,grade =self.caculate_once_value(m,n,player,value,grade)
            if is_continue:
                m, n = m-1, n+1
            else:
                break  #向右下继续移动一步     
            count +=1 

        return value if count >= 4 else 0  #如果这个方向可成5子，就返回alue，否则就是0

    def caculate_once_value(self,m,n,player,value,grade): #计算指定位置对该player价值

        loc_player = self.get_loc_player(m, n)

        if loc_player == player:
            value += grade
        elif loc_player == 0:
            value += 1     
            grade = grade/10       #碰到空棋，就降低后续的黑棋权值
        else:                      #对手的棋子 
            value -= 2    
            return 0, value, grade   # 遇到对手棋,结束后续移动    
        return 1, value, grade   


    def evaluate_all_value(self,player): #评估所有空闲位置价值

        self.move_value = defaultdict(lambda:[0,0,0,0,0])
        for move in self.board.availables:
            i,j = self.move_to_location(move)
 

            self.move_value[move][0] = self.scan_updown(i,j, player)
            self.move_value[move][1] = self.scan_leftright(i,j, player)
            self.move_value[move][2] = self.scan_left_updown(i,j, player)
            self.move_value[move][3] = self.scan_right_updown(i,j, player)
            
            #表示一个方向已经可以是冲5了       
            if (self.move_value[move][0] >= 397 or self.move_value[move][1] >= 397 or
                self.move_value[move][2] >= 397 or self.move_value[move][3] >= 397 ):
                return  move, self.max_value

            #表示一个方向已经可以是冲4了
            if (self.move_value[move][0] >= 302 or self.move_value[move][1] >= 302 or
                self.move_value[move][2] >= 302 or self.move_value[move][3] >= 302 ):
                return  move, self.max_value-100

                

            self.move_value[move][4] = self.move_value[move][0] + \
                                       self.move_value[move][1] + \
                                       self.move_value[move][2] + \
                                       self.move_value[move][3] 


        move = max(self.board.availables,key = lambda x:self.move_value[x][4])  

        return move, self.move_value[move][4]
 
    def get_move(self,board):

        self.board = board

        if self.board.currentplayer == self.board.player1:
           m_player_id = self.board.players[0]
           s_player_id = self.board.players[1]
        else:
           m_player_id = self.board.players[1]
           s_player_id = self.board.players[0]

        m_move,m_value = self.evaluate_all_value(m_player_id)
        
        logging.info("loaction:{loc},value:{value}".format(
        	         loc = self.move_to_location(m_move),value=m_value))
        
        logging.info("all_move_value:{a}".format(a=self.move_value))

        s_move,s_value = self.evaluate_all_value(s_player_id)
        
        logging.info("O_loaction:{loc},value:{value}".format(
        	          loc = self.move_to_location(s_move),value = s_value))
        logging.info("O_all_move_value:{a}".format(a=self.move_value))

        """
        for l_move in self.move_value:
            logging.info("loaction:{1},value:{2}".format(self.move_to_location(l_move),
            	         self.move_value[l_move]))
        """
        if m_value >= s_value :
            return m_move
        else:
            return s_move



class ExpertPlayer(Player):
    """AI player based on MCTS"""
    def __init__(self):
        self.expert = Expert()


    def get_action(self, board):
        sensible_moves = board.availables
        if len(sensible_moves) > 0:
            move = self.expert.get_move(board)
            return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "Expert"


if __name__ == '__main__':
    
    
    log_config()

    my_board = Board()
    play1 = ExpertPlayer()
    play2 = Human()

    my_board.start(play1, play2) 
 
