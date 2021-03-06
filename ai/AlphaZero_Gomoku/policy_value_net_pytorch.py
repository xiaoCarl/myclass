# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
import torch.optim as optim
#import torch.nn.functional as F
#from torch.autograd import Variable
import numpy as np


def set_learning_rate(optimizer, lr):
    """Sets the learning rate to the given value"""
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


class MyModule(nn.Module):
    """policy-value network module"""
    def __init__(self, board_width, board_height):
        super(MyModule, self).__init__()

        self.board_width = board_width
        self.board_height = board_height
        # common layers
        self.conv1 = nn.Sequential(
                     nn.Conv2d(4, 32, kernel_size=3, padding=1),
                     nn.ReLU(True))

        self.conv2 = nn.Sequential(
                     nn.Conv2d(32, 64, kernel_size=3, padding=1),
                     nn.ReLU(True))
        
        self.conv3 = nn.Sequential(
                     nn.Conv2d(64, 128, kernel_size=3, padding=1),
                     nn.ReLU(True))
       
       # action policy layers

        self.act_conv1 = nn.Sequential(
                         nn.Conv2d(128, 4, kernel_size=1),
                         nn.ReLU(True))
        self.act_fc1 = nn.Linear(4*board_width*board_height,
                                 board_width*board_height)
        # state value layers
        self.val_conv1 = nn.Sequential(
                         nn.Conv2d(128, 2, kernel_size=1),
                         nn.ReLU(True))
        self.val_fc1 = nn.Sequential(
                         nn.Linear(2*board_width*board_height, 64),
                         nn.ReLU(True))
        self.val_fc2 = nn.Linear(64, 1)

    def forward(self, state_input):
        # common layers
        x = self.conv1(state_input)
        x = self.conv2(x)
        x = self.conv3(x)
       
        # action policy layers
        x_act = self.act_conv1(x)
        x_act = x_act.view(-1, 4*self.board_width*self.board_height)
        x_act = nn.Softmax(dim=1)(self.act_fc1(x_act))    
        #x_act = F.log_softmax(self.act_fc1(x_act),dim=1)


        # state value layers
        x_val = self.val_conv1(x)
        x_val = x_val.view(-1, 2*self.board_width*self.board_height)
        x_val = self.val_fc1(x_val)
        x_val = torch.tanh(self.val_fc2(x_val))
        return x_act, x_val


class PolicyValueNet():
    """policy-value network """
    def __init__(self, board_width, board_height,
                 model_file=None):
        
        # Device configuration
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
 
        self.board_width = board_width
        self.board_height = board_height
        self.lr = 0.01  # coef of l2 penalty
        # the policy value net module
        self.policy_value_net = MyModule(board_width, board_height).to(self.device)

        self.loss_value = nn.MSELoss()           #回归问题
       # self.loss_policy = nn.MSELoss()          #CrossEntropyLoss() #分类问题
        self.optimizer = optim.Adam(self.policy_value_net.parameters(),lr=self.lr)

        if model_file:
            net_params = torch.load(model_file)
            self.policy_value_net.load_state_dict(net_params)

    #Categorical cross-entropy# 
    def loss_policy(self,p_probs,t_probs):
        policy_loss = -torch.mean(torch.sum(t_probs*torch.log(p_probs), 1))
        return policy_loss

    """
    def loss_value(self,p_value,t_value):
        value_loss = nn.MSELoss()(p_value,t_value)
        return loss_value
    """ 

    def policy_value(self, state_batch):
        """
        input: a batch of states
        output: a batch of action probabilities and state values
        """
        state_batch = torch.FloatTensor(state_batch)
        log_act_probs, value = self.policy_value_net(state_batch)
        act_probs = np.exp(log_act_probs.data.numpy())
        return act_probs, value.data.numpy()

    def policy_value_fn(self, board):
        """
        input: board
        output: a list of (action, probability) tuples for each available
        action and the score of the board state
        """
        legal_positions = board.availables
        current_state = np.ascontiguousarray(board.current_state().reshape(
                -1, 4, self.board_width, self.board_height))
        log_act_probs, value = self.policy_value_net(torch.from_numpy(current_state).float())
        act_probs = np.exp(log_act_probs.data.numpy().flatten())
        act_probs = zip(legal_positions, act_probs[legal_positions])
        value = value.data[0][0]
        return act_probs, value

    def train_step(self, state_batch, mcts_probs, winner_batch):
        """perform a training step"""
        # wrap in Variable
        state_batch = torch.FloatTensor(state_batch)
        mcts_probs = torch.FloatTensor(mcts_probs)
        winner_batch = torch.FloatTensor(winner_batch)

        # zero the parameter gradients
        self.optimizer.zero_grad()
        # set learning rate
        #set_learning_rate(self.optimizer, lr)

        # forward
        log_act_probs, value = self.policy_value_net(state_batch)
        # define the loss = (z - v)^2 - pi^T * log(p) + c||theta||^2
        # Note: the L2 penalty is incorporated in optimizer
        
        value_loss = self.loss_value(value.view(-1), winner_batch)

        policy_loss = self.loss_policy(log_act_probs,mcts_probs)
        print("p_probs:",log_act_probs)
        print("t_probs:",mcts_probs)
        loss = value_loss + policy_loss
        # backward and optimize
        loss.backward()
        self.optimizer.step()
        #return loss.data[0], entropy.data[0]
        #for pytorch version >= 0.5 please use the following line instead.
        return value_loss.item(),policy_loss.item()

    def get_policy_param(self):
        net_params = self.policy_value_net.state_dict()
        return net_params

    def save_model(self, model_file):
        """ save model params to file """
        net_params = self.get_policy_param()  # get model params
        torch.save(net_params, model_file)
