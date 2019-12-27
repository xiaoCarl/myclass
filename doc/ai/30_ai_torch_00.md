# torch 基本概念

## Tensor

torch的tensors（张量） ,类似于Numpy中的ndarray；可以构造1维的向量，2维的矩阵，多维的空间数据； 
新的torch版本，在定义tensors时候，如果确定requires_grad=True, 这个tensor也就是一个variable，可以求导。老的版本中，是通过类Variable来指定一个tensor为变量，再设定 requires_grad属性

## torch的特性

### 求导

```
 # Create tensors.    
 x   = torch.tensor(1., requires_grad=True)     
 w  = torch.tensor(2., requires_grad=True) 
 b   = torch.tensor(3., requires_grad=True)    

 # Build a computational graph.    
 y = w * x + b    #y = 2 * x + 3    
 
 # Compute gradients.    
 y.backward()    

 # Print out the gradients.    
 print(x.grad)     # x.grad = 2     
 print(w.grad)     # w.grad = 1     
 print(b.grad)     # b.grad = 1

```

### 与numpy相互转换

```
 import numpy as np

 np_data = np.arange(6).reshape((2, 3))
 torch_data = torch.from_numpy(np_data)
 tensor2array = torch_data.numpy()

```

### 将该张量指定到特定的设备上，如GPU 

```

 # Device configuration
 device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

 # 将网络张量指定到特定设备上
 net = MyModule().to(device)

```


### 进行各种运算：

```
torch.mm()          #乘 
torch.sin()         #正玄运算
torch.mean()        #平均值
torch.add()         #加

```

## torch神经网络包nn

1. 定义一个3 * 2的全连接网络 Y=wX+b

```         
    y1 = w00 * x1 + w01 *x2 + w02*x3 + b0
    y2 = w10 * x1 + w11 *x2  + w12*x3 + b1
``` 

```
>>> import torch    
>>> import torch.nn as nn    
>>> import numpy as np

>>> model = nn.Linear(3, 2)

```

2. 显示该线性网络的初始参数

``` 
>>> print(model)
Linear(in_features=3, out_features=2, bias=True)

>>> print(model.weight)
Parameter containing:
tensor([[ 0.2081, -0.3374, -0.2891],
        [-0.2701,  0.3834, -0.3823]], requires_grad=True)
        
>>> print(model.bias)
Parameter containing:
tensor([0.0160, 0.2574], requires_grad=True)
```


3. 如果根据一组已知的x,y值拟合（训练）上面的weight和bias参数

```
>>> x_data = torch.randn(10, 3)    
>>> y_data = torch.randn(10, 2)              #一组x,y已知的数据    


>>> y_pred = model(x_data)                  #  根据x 计算出当前的y值
>>> loss =  nn.MSELoss()(y_pred, y_data)    #  与已知y_data算误差，内置多个损失函数
>>> loss.backward()                         #  反向求导，获得各参数的导数dL/dw，dL/db， dL/dw 就是误差loss对weight的导数,  dL/db 就是误差loss对bias的导数
>>> torch.optim.SGD(model.parameters(), lr=0.01).step()   #执行一步梯度下降，沿导数反方向改变各参数的值,weight = weight - lr * dL/dw

```

4. 每次执行一次loss.backward(), 可以查看误差loss对各个参数的导数变化情况

```

>>> loss.backward()                               # 误差loss对各参数的导数
    # Print out the gradients.    
>>> print ('dL/dw: ', model.weight.grad)          # dL/dw 就是误差loss对参数weight的导数,
>>> print ('dL/db: ', model.bias.grad)            # dL/db 就是误差loss对参数bias的导数

```

5. 完整的训练会一般有多组数据，整个过程如下

```

>>> optimizer =torch.optim.SGD(model.parameters(), lr=0.01)
>>> criterion = nn.MSELoss()  

>>> for epoch in range(100):
.  .  .      y_pred = model(x_data)
.  .  .      loss =criterion(y_pred, y_data)         # 计算两者的误差
.  .  .      optimizer.zero_grad()                   # 清空上一步的残余更新参数值
.  .  .      loss.backward()                         # 误差反向传播, 计算参数更新值
.  .  .      optimizer.step()                        # 将参数更新值施加到linear 的 parameters
.  .  .      if (epoch+1) % 5 == 0:    
.  .  .          print ('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, 100, loss.item()))

```

6. 在测试的时候，如果不需要tensor求导，为了节约内存，使用以下语句：

```
 with torch.no_grad(): 
        

```







