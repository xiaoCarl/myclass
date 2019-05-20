import numpy as np

from load_data import load_sas_data
from multi_net import MultiLayerNet

(x_train,y_train) = load_sas_data()

network = MultiLayerNet(input_size=23,hidden_size_list=[18,12],output_size=6)

iters_num = 50
train_size = x_train.shape[0]
batch_size = 131
learning_rate = 0.1

for i in range(iters_num):
    batch_mask = np.random.choice(train_size,batch_size)
    x_batch = x_train[batch_mask]
    y_batch = y_train[batch_mask]

    grads = network.gradient(x_batch,y_batch)

    for key in network.params.keys():
        network.params[key] -= learning_rate*grads[key] 
       

    train_acc = network.accuracy(x_train,y_train)
    print("train acc: " + str(train_acc) )



