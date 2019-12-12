# -*- coding: utf-8 -*-
import numpy as np
import copy
from operator import itemgetter
import datetime

def rollout_policy_fn(board):
    action_probs = np.random.rand(len(board.available))
    return zip(board.available, action_probs)

def policy_value_fn(board):
    """a function that takes in a board and outputs a list of (action, probability) tuples and a score for the board"""
    # return uniform probabilities and 0 score for pure MCTS
    probs = np.ones(len(board.available))/len(board.available)
    # probs = np.random.random(len(board.available))
    # max_action = board.available[int(np.argwhere(probs==np.max(probs)))] #取最大值对应的下标值
    action_probs =  zip(board.available,probs)
    return action_probs,0

class TreeNode(object):
    """A node in the MCTS tree. Each node keeps track of its own value Q,
    prior probability P, and its visit-count-adjusted prior score u.
    """

    def __init__(self, parent, prior_p):
        self._parent = parent
        self._children = {}  # dict action:TreeNode
        self._N = 0          #记录节点的访问次数
        self._W = 0          #节点总的价值            
        self._Q = 0          #节点平均价值     
        self._P = prior_p    #选择该节点的给予的概率 

    def update(self, leaf_value):
        # Count visit.
        self._N += 1
        self._W += leaf_value
        # Update Q, a running average of values for all visits.
        self._Q = self._W/self._N

    def get_value(self, c_puct):
        return self._Q + self._P*c_puct * np.sqrt(np.log(self._parent._N)/(self._N+1e-3))

    def is_leaf(self):
        return self._children == {}

    def is_root(self):
        return self._parent is None


class MCTS(object):
    """A simple implementation of Monte Carlo Tree Search."""

    def __init__(self, policy_value_fn, c_puct=5, simulate_time=10,n_playout=500):
        """
        policy_value_fn:策略函数
        c_puct :控制深度优先，还是广度优先。参见UCB公式
        simulate_time:每次模拟时间，单位是秒
        """
        self._root = TreeNode(None, 1.0)
        self._root._N = 0
        self._policy = policy_value_fn
        self._c_puct = c_puct
        self.simulate_time = datetime.timedelta(seconds=simulate_time)
        self._n_playout = n_playout

    def _selection(self,board):
        node = self._root
        while not node.is_leaf():
            # Greedily select next move.
            action, node = max(node._children.items(),
                               key=lambda act_node: act_node[1].get_value(self._c_puct))
            board.do_move(action)
            #set_action(action)
            #board.next_states()
        return board,node

    def _expansion(self,board,node):
        action_probs,leaf_value= self._policy(board)
        #extand all children node
        for action,probs in action_probs:
            if action not in node._children:
                node._children[action] = TreeNode(node, probs)
        return leaf_value

    def _backpropagation(self,node,leaf_value):
        # Update value and visit count of nodes in this traversal.
        node.update(leaf_value)
        while node._parent :
            node = node._parent
            leaf_value = -leaf_value
            node.update(leaf_value)

    def _playout(self,board):
        # Selection
        board, node = self._selection(board)
        # Expansion 
        # 
        leaf_value = self._expansion(board,node)
        # Simulation
        #leaf_value = self._simulation(board)
        # Backpropagation
        self._backpropagation(node,leaf_value)
    
    def get_move_probs(self, board, temper=0.01):
        """self player use
        """
        for n in range(self._n_playout):
            board_copy = copy.deepcopy(board)
            self._playout(board_copy)

        # calc the move probabilities based on visit counts at the root node
        act_visits = [(act, node._N) for act, node in self._root._children.items()]
        acts, visits = zip(*act_visits)
        act_probs = self.soft_max(1.0/temper * np.log(np.array(visits) + 1e-10))

        #print(acts,act_probs) 
        return acts, act_probs
    
    def soft_max(self,x):
         probs = np.exp(x - np.max(x))
         #probs = np.exp(x-1)
         probs /= np.sum(probs)
         return probs
    
    def update_with_move(self,last_move):
        if last_move in self._root._children:
            self._root = self._root._children[last_move]
            self._root._parent = None
        else:
            self._root = TreeNode(None, 1.0)

    def __str__(self):
        return "MCTS"

class AlphaZeroPlayer(object):
    """AI player based on MCTS"""

    def __init__(self, policy_value_function,
                 c_puct=5, n_playout=2000, is_selfplay=0):
        self.mcts = MCTS(policy_value_function, c_puct, n_playout)
        self._is_selfplay = is_selfplay

    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_temperature(self,board):
        if self._is_selfplay:
            temper = 1e-3 
        else: # 选择温度参数
            if len(board.availables) > 60:
                temper = 1.0
            elif len(board.availables)> 56:
                temper = 0.5
            elif len(board.availables)> 48:
                temper = 1e-1
            elif len(board.availables)> 42:
                temper = 1e-2
            else:
                temper = 1e-3 
        return temper   

    def get_action(self, board, return_prob=0):
        sensible_moves = board.availables
        # the pi vector returned by MCTS as in the alphaGo Zero paper
        move_probs = np.zeros(board.width*board.height)
      
        # 选择温度参数
        temper = self.get_temperature(board)
        if len(sensible_moves) > 0:
            acts, probs = self.mcts.get_move_probs(board, temper)
            move_probs[list(acts)] = probs
            if self._is_selfplay:
                # add Dirichlet Noise for exploration (needed for
                # self-play training)
                move = np.random.choice(
                    acts,
                    p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
                )
                # update the root node and reuse the search tree
                self.mcts.update_with_move(move)
            else:
                # with the default temp=1e-3, it is almost equivalent
                # to choosing the move with the highest prob
                move = np.random.choice(acts, p=probs)
                # reset the root node
                self.mcts.update_with_move(-1)
#                location = board.move_to_location(move)
#                print("AI move: %d,%d\n" % (location[0], location[1]))

            if return_prob:
                return move, move_probs
            else:
                return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "AlphaZero {}".format(self.player)
