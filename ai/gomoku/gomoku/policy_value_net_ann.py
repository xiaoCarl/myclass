# coding: utf-8
import pickle
import numpy as np
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

def cross_entropy_error(y, t):
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
        
    if t.size == y.size:
        t = t.argmax(axis=1)
             
    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size

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
        
        dx = dx.reshape(*self.original_x_shape)  # 入力データの形状に戻す（テンソル対応）
        return dx

class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None
        self.y = None # softmaxの出力
        self.t = None # 教師データ

    def forward(self, x, t):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y, self.t)
        
        return self.loss

    def backward(self, dout=1):
        batch_size = self.t.shape[0]
        if self.t.size == self.y.size: # 教師データがone-hot-vectorの場合
            dx = (self.y - self.t) / batch_size
        else:
            dx = self.y.copy()
            dx[np.arange(batch_size), self.t] -= 1
            dx = dx / batch_size
        
        return dx

class MultiLayerNet:
    """
    Parameters
    ----------
    input_size : 
    hidden_size_list : （e.g. [100, 100, 100]）
    output_size : [0,1,...,30,>30]
    activation : 'relu' or 'sigmoid'
    weight_init_std : 
        'relu'
        'sigmoid'
    """
    def __init__(self, input_size, hidden_size_list, output_size,
                 activation='relu', weight_init_std='relu', weight_decay_lambda=0):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size_list = hidden_size_list
        self.hidden_layer_num = len(hidden_size_list)
        self.weight_decay_lambda = weight_decay_lambda
        self.params = {}

        self.__init_weight(weight_init_std)

        activation_layer = {'sigmoid': Sigmoid, 'relu': Relu}
        self.layers = OrderedDict()
        for idx in range(1, self.hidden_layer_num+1):
            self.layers['Affine' + str(idx)] = Affine(self.params['W' + str(idx)],
                                                      self.params['b' + str(idx)])
            self.layers['Activation_function' + str(idx)] = activation_layer[activation]()

        idx = self.hidden_layer_num + 1
        self.layers['Affine' + str(idx)] = Affine(self.params['W' + str(idx)],
            self.params['b' + str(idx)])

        self.last_layer = SoftmaxWithLoss()

    def __init_weight(self, weight_init_std):

        all_size_list = [self.input_size] + self.hidden_size_list + [self.output_size]
        for idx in range(1, len(all_size_list)):
            scale = weight_init_std
            if str(weight_init_std).lower() in ('relu', 'he'):
                scale = np.sqrt(2.0 / all_size_list[idx - 1])  # ReLUを使う場合に推奨される初期値
            elif str(weight_init_std).lower() in ('sigmoid', 'xavier'):
                scale = np.sqrt(1.0 / all_size_list[idx - 1])  # sigmoidを使う場合に推奨される初期値

            self.params['W' + str(idx)] = scale * np.random.randn(all_size_list[idx-1], all_size_list[idx])
            self.params['b' + str(idx)] = np.zeros(all_size_list[idx])

    def predict(self, x):
        for layer in self.layers.values():
            x = layer.forward(x)

        return x

    def loss(self, x, t):
        y = self.predict(x)

        weight_decay = 0
        for idx in range(1, self.hidden_layer_num + 2):
            W = self.params['W' + str(idx)]
            weight_decay += 0.5 * self.weight_decay_lambda * np.sum(W ** 2)

        return self.last_layer.forward(y, t) + weight_decay

    def accuracy(self, x, t):
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        if t.ndim != 1 : t = np.argmax(t, axis=1)

        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy

    def gradient(self, x, t):
        self.loss(x, t)

        # backward
        dout = 1
        dout = self.last_layer.backward(dout)

        layers = list(self.layers.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)

        grads = {}
        for idx in range(1, self.hidden_layer_num+2):
            grads['W' + str(idx)] = self.layers['Affine' + str(idx)].dW + self.weight_decay_lambda * self.layers['Affine' + str(idx)].W
            grads['b' + str(idx)] = self.layers['Affine' + str(idx)].db

        return grads

class PolicyValueNet():
    def __init__(self, board_width, board_height, model_file=None):
        self.board_size = board_width*board_height
        input_size = self.board_size*4
        probs_hidden_size_list = [self.board_size*3, self.board_size*2]
        probs_output_size = self.board_size

        value_hidden_size_list = [self.board_size*3, self.board_size*1]
        value_output_size = 1

        self.network_probs = MultiLayerNet(input_size = input_size,
                             hidden_size_list = probs_hidden_size_list,
                             output_size = probs_out_size)
        self.network_value = MultiLayerNet(input_size = input_size,
                             hidden_size_list = value_hidden_size_list,
                             output_size = value_output_size)

        if model_file is not None:
            self.load_model(model_file)


    def policy_value_fn(self, board):
        legal_positions = board.availables
        current_state = board.current_state()

        x = current_state.reshape(-1, 4*self.board_size)
        probs = self.network_probs.predict(x)
        act_probs = zip(legal_positions, probs.flatten()[legal_positions])

        value =  self.network_value.predict(x)
        
        return act_probs, value


    def policy_value(self, x):
        
        x = x.reshape(-1, 4*self.board_size)
        probs = self.network_probs.predict(x)

        value =  self.network_value.predict(x)
        
        return probs, value
    
    
    def train_step(self, state_batch, mcts_probs, winner_batch, lr):

        state_batch = np.reshape(state_batch,(-1,4*self.board_size))
        mcts_probs = np.reshape(mcts_probs, (-1, self.board_size))
        winner_batch = np.reshape(winner_batch, (-1, 1))
    
        probs_grads = self.network_probs.gradient(state_batch,mcts_batch)
        probs_loss  = self.network_probs.loss(state_batch,mcts_batch)
        for key in self.network_probs.params.keys():
            self.network_probs.params[key] -= lr*probs_grads[key] 

        value_grads = self.network_value.gradient(state_batch,winner_batch)
        value_loss  = self.network_value.loss(state_batch,winner_batch)

        for key in self.network_value.params.keys():
            self.network_value.params[key] -= lr*value_grads[key] 
        
        return probs_loss, value_loss
   
   def save_model(self, model_name="params.pkl"):
        params = {}
        params['network_probs'] = {} 
        params['network_value'] = {} 

        for key, val in self.network_probs.params.items():
            params['network_probs'][key] = val
        for key, val in self.network_value.params.items():
            params['network_value'][key] = val

        with open(model_name, 'wb') as f:
            pickle.dump(params, f)

    def load_model(self, model_name="params.pkl"):
        with open(model_name, 'rb') as f:
            params = pickle.load(f)
        
        for key, val in params['network_probs'].items():
            self.network_probs.params[key] = val

        for key, val in params['network_value'].items():
            self.network_value.params[key] = val

        for i, key in enumerate(['Affine1', 'Affine2','Affine3','Affine4']):
            self.network_value.layers[key].W = self.network_value.params['W' + str(i+1)]
            self.network_value.layers[key].b = self.network_value.params['b' + str(i+1)]
            self.network_probs.layers[key].W = self.network_probs.params['W' + str(i+1)]
            self.network_probs.layers[key].b = self.network_value.params['b' + str(i+1)]