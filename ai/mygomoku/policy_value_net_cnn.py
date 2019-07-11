# -*- coding: utf-8 -*-
"""
Implement the policy value network using numpy, so that we can play with the
trained AI model without installing any DL framwork
"""

from __future__ import print_function
import numpy as np
import pickle
from collections import OrderedDict


def sigmoid(x):
    return 1 / (1 + np.exp(-x))    

def relu(x):
    return np.maximum(0, x)

def softmax(x):
    if x.ndim == 2:
        x = x.T
        x = x - np.max(x, axis=0)
        y = np.exp(x) / np.sum(np.exp(x), axis=0)
        return y.T 

    x = x - np.max(x) 
    return np.exp(x) / np.sum(np.exp(x))

def mean_squared_error(y, t):
    return 0.5 * np.sum((y-t)**2)

def cross_entropy_error(y, t):
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
        
    if t.size == y.size:
        t = t.argmax(axis=1)
             
    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size


def im2col(input_data, filter_h, filter_w, stride=1, pad=0):

    N, C, H, W = input_data.shape
    out_h = (H + 2*pad - filter_h)//stride + 1
    out_w = (W + 2*pad - filter_w)//stride + 1

    img = np.pad(input_data, [(0,0), (0,0), (pad, pad), (pad, pad)], 'constant')
    col = np.zeros((N, C, filter_h, filter_w, out_h, out_w))

    for y in range(filter_h):
        y_max = y + stride*out_h
        for x in range(filter_w):
            x_max = x + stride*out_w
            col[:, :, y, x, :, :] = img[:, :, y:y_max:stride, x:x_max:stride]

    col = col.transpose(0, 4, 5, 1, 2, 3).reshape(N*out_h*out_w, -1)
    return col

def col2im(col, input_shape, filter_h, filter_w, stride=1, pad=0):
    N, C, H, W = input_shape
    out_h = (H + 2*pad - filter_h)//stride + 1
    out_w = (W + 2*pad - filter_w)//stride + 1
    col = col.reshape(N, out_h, out_w, C, filter_h, filter_w).transpose(0, 3, 4, 5, 1, 2)

    img = np.zeros((N, C, H + 2*pad + stride - 1, W + 2*pad + stride - 1))
    for y in range(filter_h):
        y_max = y + stride*out_h
        for x in range(filter_w):
            x_max = x + stride*out_w
            img[:, :, y:y_max:stride, x:x_max:stride] += col[:, :, y, x, :, :]

    return img[:, :, pad:H + pad, pad:W + pad]


class Relu:
    def __init__(self):
        self.mask = None

    def forward(self, x):
        
        self.mask = (x <= 0)
        
        out = x.copy()
        out[self.mask] = 0

        return out

    def backward(self, dout):
        dout[self.mask] = 0
        dx = dout

        return dx

class Sigmoid:
    def __init__(self):
        self.out = None

    def forward(self, x):
        out = sigmoid(x)
        self.out = out
        return out

    def backward(self, dout):
        dx = dout * (1.0 - self.out) * self.out

        return dx

class Affine:
    def __init__(self, W, b):
        self.W =W
        self.b = b
        
        self.x = None
        self.original_x_shape = None
        self.dW = None
        self.db = None

    def forward(self, x):
        self.original_x_shape = x.shape
        x = x.reshape(x.shape[0], -1)
        self.x = x

        out = np.dot(self.x, self.W) + self.b

        return out

    def backward(self, dout):
        dx = np.dot(dout, self.W.T)
        self.dW = np.dot(self.x.T, dout)
        self.db = np.sum(dout, axis=0)
        
        dx = dx.reshape(*self.original_x_shape)  
        return dx

class MeanSquaredWithLoss:
    def __init__(self):
        self.loss = None
        self.y = None 
        self.t = None 

    def forward(self, x, t):
        self.t = t
        self.y = x
        self.loss = mean_squared_error(self.y, self.t)
        
        return self.loss

    def backward(self, dout=1):
        batch_size = self.t.shape[0]
        if self.t.size == self.y.size:
            dx = (self.y - self.t) / batch_size
        else:
            dx = self.y.copy()
            dx[np.arange(batch_size), self.t] -= 1
            dx = dx / batch_size
        
        return dx

class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None
        self.y = None 
        self.t = None 

    def forward(self, x, t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y, self.t)
        
        return self.loss

    def backward(self, dout=1):
        batch_size = self.t.shape[0]
        if self.t.size == self.y.size:
            dx = (self.y - self.t) / batch_size
        else:
            dx = self.y.copy()
            dx[np.arange(batch_size), self.t] -= 1
            dx = dx / batch_size
        
        return dx

class Convolution:
    def __init__(self, W, b, stride=1, pad=0):
        self.W = W
        self.b = b
        self.stride = stride
        self.pad = pad
        
        self.x = None   
        self.col = None
        self.col_W = None
        
        self.dW = None
        self.db = None

    def forward(self, x):
        FN, C, FH, FW = self.W.shape
        N, C, H, W = x.shape
        out_h = 1 + int((H + 2*self.pad - FH) / self.stride)
        out_w = 1 + int((W + 2*self.pad - FW) / self.stride)

        col = im2col(x, FH, FW, self.stride, self.pad)
        col_W = self.W.reshape(FN, -1).T

        out = np.dot(col, col_W) + self.b
        out = out.reshape(N, out_h, out_w, -1).transpose(0, 3, 1, 2)

        self.x = x
        self.col = col
        self.col_W = col_W

        return out

    def backward(self, dout):
        FN, C, FH, FW = self.W.shape
        dout = dout.transpose(0,2,3,1).reshape(-1, FN)

        self.db = np.sum(dout, axis=0)
        self.dW = np.dot(self.col.T, dout)
        self.dW = self.dW.transpose(1, 0).reshape(FN, C, FH, FW)

        dcol = np.dot(dout, self.col_W.T)
        dx = col2im(dcol, self.x.shape, FH, FW, self.stride, self.pad)

        return dx


class Pooling:
    def __init__(self, pool_h, pool_w, stride=1, pad=0):
        self.pool_h = pool_h
        self.pool_w = pool_w
        self.stride = stride
        self.pad = pad
        
        self.x = None
        self.arg_max = None

    def forward(self, x):
        N, C, H, W = x.shape
        out_h = int(1 + (H - self.pool_h) / self.stride)
        out_w = int(1 + (W - self.pool_w) / self.stride)

        col = im2col(x, self.pool_h, self.pool_w, self.stride, self.pad)
        col = col.reshape(-1, self.pool_h*self.pool_w)

        arg_max = np.argmax(col, axis=1)
        out = np.max(col, axis=1)
        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)

        self.x = x
        self.arg_max = arg_max

        return out

    def backward(self, dout):
        dout = dout.transpose(0, 2, 3, 1)
        
        pool_size = self.pool_h * self.pool_w
        dmax = np.zeros((dout.size, pool_size))
        dmax[np.arange(self.arg_max.size), self.arg_max.flatten()] = dout.flatten()
        dmax = dmax.reshape(dout.shape + (pool_size,)) 
        
        dcol = dmax.reshape(dmax.shape[0] * dmax.shape[1] * dmax.shape[2], -1)
        dx = col2im(dcol, self.x.shape, self.pool_h, self.pool_w, self.stride, self.pad)
        
        return dx


"""
   conv - relu - pool - affine - relu - affine - softmax
   conv - relu - pool - affine - relu - affine - softmax
 
"""
class PolicyValueNet():
    def __init__(self, board_width, board_height, model_file=None):
        self.board_width = board_width
        self.board_height = board_height
        input_dim = (4, board_width, board_height) 
        conv_param = {'filter_num':32, 'filter_size':3, 'pad':0, 'stride':1}
        filter_num = conv_param['filter_num']
        filter_size = conv_param['filter_size']
        filter_pad = conv_param['pad']
        filter_stride = conv_param['stride']
        input_size = input_dim[1]
        conv_output_size = (input_size - filter_size + 2*filter_pad) / filter_stride + 1
        pool_output_size = int(filter_num * (conv_output_size/2) * (conv_output_size/2))
        
        hidden_size_probs = 256
        output_size_probs = board_width * board_height
        hidden_size_value = 128
        output_size_value = 3 
        weight_init_std = 0.01
         
        #define policy net 
        self.params_p = {}
        self.params_p['W1'] = weight_init_std * \
                            np.random.randn(filter_num, input_dim[0], filter_size, filter_size)
        self.params_p['b1'] = np.zeros(filter_num)
        self.params_p['W2'] = weight_init_std * \
                            np.random.randn(pool_output_size, hidden_size_probs)
        self.params_p['b2'] = np.zeros(hidden_size_probs)
        self.params_p['W3'] = weight_init_std * \
                            np.random.randn(hidden_size_probs, output_size_probs)
        self.params_p['b3'] = np.zeros(output_size_probs)

        self.layers_p = OrderedDict()
        self.layers_p['Conv1'] = Convolution(self.params_p['W1'], self.params_p['b1'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers_p['Relu1'] = Relu()
        self.layers_p['Pool1'] = Pooling(pool_h=2, pool_w=2, stride=2)
        self.layers_p['Affine1'] = Affine(self.params_p['W2'], self.params_p['b2'])
        self.layers_p['Relu2'] = Relu()
        self.layers_p['Affine2'] = Affine(self.params_p['W3'], self.params_p['b3'])
        self.last_layer_p = SoftmaxWithLoss()

        #define value net
        self.params_v = {}
        self.params_v['W1'] = weight_init_std * \
                            np.random.randn(filter_num, input_dim[0], filter_size, filter_size)
        self.params_v['b1'] = np.zeros(filter_num)
        self.params_v['W2'] = weight_init_std * \
                            np.random.randn(pool_output_size, hidden_size_value)
        self.params_v['b2'] = np.zeros(hidden_size_value)
        self.params_v['W3'] = weight_init_std * \
                            np.random.randn(hidden_size_value, output_size_value)
        self.params_v['b3'] = np.zeros(output_size_value)
         
        self.layers_v = OrderedDict()
        self.layers_v['Conv1'] = Convolution(self.params_v['W1'], self.params_v['b1'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers_v['Relu1'] = Relu()
        self.layers_v['Pool1'] = Pooling(pool_h=2, pool_w=2, stride=2)
        self.layers_v['Affine1'] = Affine(self.params_v['W2'], self.params_v['b2'])
        self.layers_v['Relu2'] = Relu()
        self.layers_v['Affine2'] = Affine(self.params_v['W3'], self.params_v['b3'])
        self.last_layer_v = SoftmaxWithLoss()

        if model_file is not None:
            self.load_model(model_file)


    def policy_value_fn(self, board):
        legal_positions = board.availables
        current_state = board.current_state()

        x = current_state.reshape(-1, 4, self.board_width, self.board_height)

        probs,value = self.policy_value(x) 
        
        act_probs = zip(legal_positions, probs.flatten()[legal_positions])
        
        m_value = value[0]
        
        if m_value[0] == max(m_value):
            act_value = 0
        elif m_value[1] == max(m_value):
            act_value = 1.0
        else:
            act_value = -1.0        

        return act_probs,act_value


    def policy_value(self, x):
        
        x = np.reshape(x,(-1,4,self.board_width, self.board_height))

        probs = x
        for layer_probs in self.layers_p.values():
            probs = layer_probs.forward(probs)

        value = x
        for layer_value in self.layers_v.values():
            value =layer_value.forward(value)

        return probs, value 

    def loss(self, x, probs,value):
        p_probs,p_value  = self.policy_value(x)
        loss_probs = self.last_layer_p.forward(p_probs, probs)
        loss_value = self.last_layer_v.forward(p_value, value)
        return loss_probs, loss_value

    def gradient(self, x, probs, value):
        
        # forward
        self.loss(x, probs,value)
        #print("probs：{},value:{}".format(probs,value))  
        # probs network backward  
        dout = 1
        dout = self.last_layer_p.backward(dout)

        layers = list(self.layers_p.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)

        grads_p = {}
        grads_p['W1'], grads_p['b1'] = self.layers_p['Conv1'].dW, self.layers_p['Conv1'].db
        grads_p['W2'], grads_p['b2'] = self.layers_p['Affine1'].dW, self.layers_p['Affine1'].db
        grads_p['W3'], grads_p['b3'] = self.layers_p['Affine2'].dW, self.layers_p['Affine2'].db

        # value network backward  
        dout = 1
        dout = self.last_layer_v.backward(dout)
        #print("dout:{}".format(dout))

        layers = list(self.layers_v.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)

        grads_v = {}
        grads_v['W1'], grads_v['b1'] = self.layers_v['Conv1'].dW, self.layers_v['Conv1'].db
        grads_v['W2'], grads_v['b2'] = self.layers_v['Affine1'].dW, self.layers_v['Affine1'].db
        grads_v['W3'], grads_v['b3'] = self.layers_v['Affine2'].dW, self.layers_v['Affine2'].db

        return grads_p, grads_v


   
    def train_step(self, state_batch, mcts_probs, winner_batch, lr):
        
        state_batch = np.reshape(state_batch,(-1,4,self.board_width, self.board_height))
        mcts_probs = np.reshape(mcts_probs, (-1, self.board_width*self.board_height))
        winner_batch = np.reshape(winner_batch, (-1, 3))

        grads_p,grads_v = self.gradient(state_batch, mcts_probs, winner_batch)
        
        for key in self.params_p.keys():
            self.params_p[key] -= lr*grads_p[key] 

        for key in self.params_v.keys():
            self.params_v[key] -= lr*grads_v[key] 

        loss_probs,loss_value = self.loss(state_batch, mcts_probs, winner_batch)
        return loss_probs, loss_value
    
    def save_model(self, model_name="params.pkl"):
        params = {}
        params["params_p"]={}
        params["params_v"]={}
      
        for key, val in self.params_p.items():
            params["params_p"][key] = val
        for key, val in self.params_v.items():
            params["params_v"][key] = val

        with open(model_name, 'wb') as f:
            pickle.dump(params, f)

    def load_model(self, model_name="params.pkl"):
        with open(model_name, 'rb') as f:
            params = pickle.load(f)

        for key, val in params["params_p"].items():
            self.params_p[key] = val
        for key, val in params["params_v"].items():
            self.params_v[key] = val

        for i, key in enumerate(['Conv1', 'Affine1', 'Affine2']):
            self.layers_p[key].W = self.params_p['W' + str(i+1)]
            self.layers_p[key].b = self.params_p['b' + str(i+1)]
            self.layers_v[key].W = self.params_v['W' + str(i+1)]
            self.layers_v[key].b = self.params_v['b' + str(i+1)]