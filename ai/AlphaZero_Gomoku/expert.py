# encoding: utf-8
#from player import Player
from game import Board

from collections import defaultdict
import logging
from mcts_alphaZero import MCTSPlayer
import numpy as  np
import random
import heapq

class Expert(object):
    def __init__(self):
        self.grade  = 100            #同一色棋子的权重
        self.max_value = 10012345    #表示已经已经冲5，达到最大权重

    def location_to_move(self,i,j):
        """location = (i,j),move=i+j*width 
        """
        return i+j*self.board.width

    def move_to_location(self,move):
        """location = (i,j),dot=i+j*width 
        """
        i = move % self.board.width
        j = move // self.board.height
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
        while m < self.board.width and n < self.board.height:
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
        while m < self.board.width and n >=0:
            is_continue,value,grade =self.caculate_once_value(m,n,player,value,grade)
            if is_continue:
                m, n = m+1, n-1
            else:
                break  #向右上继续移动一步     
            count +=1 

        grade=self.grade
        m, n = i-1, j+1   #向右下      
        while m >=0 and n < self.board.height:
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
            value -= 5    
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
            
            #表示一个方向已经可以是冲5了: 最差分数模式：XOO-OOX :396
            # XOOOO-X :396 ;      
            """   
            if (self.move_value[move][0] >= 390 or self.move_value[move][1] >= 390 or
                self.move_value[move][2] >= 390 or self.move_value[move][3] >= 390 ):
                return  move, self.max_value
            """

            #表示一个方向已经可以是冲4了
            for k in range(4):
               if self.move_value[move][k] >= 390 :
                   self.move_value[move][k] = 2000
               elif self.move_value[move][k] >= 302 :
                   self.move_value[move][k] = 1000

                
            #综合各个方向得分
            self.move_value[move][4] = self.move_value[move][0] + \
                                       self.move_value[move][1] + \
                                       self.move_value[move][2] + \
                                       self.move_value[move][3] + \
                                       3 


        
        max_value = max(self.move_value[i][4] for i in self.board.availables)

        value_sum = sum(self.move_value[i][4] for i in self.board.availables )      

        print(self.move_value)
        if value_sum == 0: value_sum=1
        probs = np.zeros(self.board.width*self.board.height)

        move_list=[]
        for i in range(self.board.width*self.board.height): #计算每个位置的概率
            probs[i] = 1.0*self.move_value[i][4]/value_sum
            
        if len(self.board.availables) > 3:
            move_list = heapq.nlargest(3,self.move_value,key=lambda i : self.move_value[i][4])
            print(move_list)
       
            move = random.choice(move_list) 
        else:
            move = random.choice(self.board.availables)            
          
        print(move)
        return move, self.move_value[move][4], probs
 
    def get_move(self,board):
        self.board = board        

        if self.board.get_current_player() == self.board.players[0]:
           m_player_id = self.board.players[0]
           s_player_id = self.board.players[1]
        else:
           m_player_id = self.board.players[1]
           s_player_id = self.board.players[0]

        m_move,m_value,m_probs = self.evaluate_all_value(m_player_id)
        
#        logging.info("loaction:{loc},value:{value}, probs:{probs}".format(
#        	         loc = self.move_to_location(m_move),value=m_value, probs=m_probs))
        
        s_move,s_value,s_probs = self.evaluate_all_value(s_player_id)
        
#        logging.info("O_loaction:{loc},value:{value}, probs:{probs}".format(
#        	          loc = self.move_to_location(s_move),value = s_value,probs=s_probs))

        if m_value >= s_value :
            return m_move ,m_probs
        else:
            return s_move ,s_probs

class ExpertPlayer(object):
    """AI player based on Expert"""
    def __init__(self,mcts_player=0,is_selfplay=0):
        self.expert = Expert()
        self.is_selfplay = is_selfplay
        if is_selfplay:
            self.mcts_player= mcts_player

    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts_player.mcts.update_with_move(-1)
    

    def get_action(self, board, temp=0, return_prob=0):
        sensible_moves = board.availables
        if len(sensible_moves) > 0:
            move,probs = self.expert.get_move(board)
            print(move)
            if self.is_selfplay:
                self.mcts_player.mcts.update_with_move(move) #update mcts tree node
            if return_prob:
                return move, probs
            else:
                return move

        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "Expert"

