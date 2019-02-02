import numpy as np


m = 5

x0_data = np.ones((m, 1))
x1_data = np.float32(np.random.rand(2, m)).reshape(m,2) 
x_data  = np.hstack((x0_data, x1_data))

y_data  = np.dot(x_data, [0.300, 0.100, 0.200])

'''
y_data1 = np.dot(x_data,[0,100,0.200]) + 0.300 
Y = W * X + b
W=[0.100,0.200]
b=0.300

theta =[0.300,0.100,0.200]
Y = theta * X

'''

'''
 Training  Set:
       Y          X
       y_data,  x_data
  
  Hypothesis:
       Y = theta * X
       
 slove :
       theta
'''

'''
Loss or Cost function
X_data.shape=(m,3)
theta.shape =(3,)
Y_data.shape=(m,)
'''
def loss_function(theta, X_data, Y_data):
    '''Cost function J definition.'''
    diff = np.dot(X_data, theta) - Y_data
    num = np.size(Y_data)
    return (1./2*num) * np.dot(np.transpose(diff), diff)


'''gradient function
'''
def gradient_function(theta, X_data, Y_data):
    '''Gradient of the function J definition.'''
    diff = np.dot(X_data,theta) - Y_data
    num = np.size(Y_data)
    return (1./num) * np.dot(np.transpose(X_data), diff)


'''get min point
'''
def gradient_descent(X_data, Y_data, optimizer,theta):
    '''Perform gradient descent.'''
    gradient = gradient_function(theta, X_data, Y_data)
    while not np.all(np.absolute(gradient) <= 1e-5):
        theta = theta - optimizer * gradient
        gradient = gradient_function(theta, X_data, Y_data)
    return theta    


def train(X_data,Y_data,optimizer,theta):
    gradient = gradient_function(theta, X_data, Y_data)
    theta = theta - optimizer * gradient
    return theta


optimizer = 0.5
theta = np.array([1, 1, 1]).reshape(3,) #init thera

#gradient_descent(x_data, y_data, optimizer,theta)

for step in xrange(0, 1001):
    theta = train(x_data, y_data, optimizer,theta)
    if step % 20 == 0:
        print(step, theta)
