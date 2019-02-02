
# 相关文件说明

## np_tf_demo.py 
  这是用numpy写的一个线性回归算法，采用梯度下降的算法，可以对照tensorflow的文件对比看

### loss_function(theta, X_data, Y_data):
  以矩阵向量的形式定义代价（或者损失）函数，采用的均方误差代价函数

### gradient_function(theta, X_data, Y_data):
  代价函数的梯度,对theta向量求导

### gradient_descent(X_data, Y_data, optimizer,theta)
  根据最小步长(学习率）optimizer,初始theta值，梯度下降迭代计算，当梯度小于1e-5时，说明已经进入了比较平滑的状态，类似于山谷的状态，这时候再继续迭代效果也不大了，所以这个时候可以退出循环！

### train(X_data,Y_data,optimizer,theta):
   通过梯度函数,单步训练
   theta1 = theta0(当前值) - optimizer(步长）* gradient_function(梯度函数) 

## tf_dgrad.py 
这是用tensor写的一个采用梯度下降的算法，tensor官网提供


## tf_mnist_1.py
基于线性回归算法的数字识别，准确率90%左右，tensor官网提供

## tf_mnist_2.py
基于神经网络的简单手写识别算法框架，准确率超过99%，tensor 官网提供

## 完整的CNN例子
mnist.py
input_data.py
full_connected_feed.py 
一个完整的CNN 深度学习算法的框架,准确率超过99%，tensor官网提供



