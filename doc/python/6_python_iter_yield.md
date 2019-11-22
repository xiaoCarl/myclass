# 迭代器，生成器(yield)

带有yield的函数，在Python中称之为生成器generator

## 看一个例子：
斐波那契数列是一个非常简单的递归数列，除第一个，第二个数外，任意一个数都可由前两个数相加得到、

def fab(max):

         n,a,b = 0,0,1

         while n < max:

                print b

                a,b=b,a+b

                n=n+1

为了提高函数的可复用性，不直接打印，返回一个list 

def fab(max):

         n,a,b = 0,0,1

         l = list()

         while n < max:

                l.append(b)

                a,b=b,a+b

                n=n+1

          return l

该函数在运行的时候，占用的内存会随参数max的增大而增大，如果要控制内存占用，不能用list来保存结果，可以使用iterable对象来迭代：

class Fab(object):

      def __init__(self,max):

             self.max=max

             self.n,self.a,self.b = 0,0,1

     def __iter__(self):

           return self

     def next(self):

            if self.n <self.max:

                r= self.b

                self.a,self.b = self.b ,self.a+self.b

                self.n = self.n+1

                return r

           raise StopIterarion()



使用class改写的版本，代码远远没有第一个版本的fab函数来得简洁，如果我们想要保持第一个版本的fab函数简洁性，同时又要获得iterable的效果，yield派上用场

def fab(max):

         n,a,b = 0,0,1

         while n < max:

                yield b            #将第一个版本的print b 修改为yield b ，就将整个函数变成了一个生成器。

                a,b=b,a+b

                n=n+1



带有yield的函数不再是一个普通函数，python解释器会将其视为一个生成器generator.  generator只有对其调用next()的时候，才开始执行。 备注：for循环会自动调用next()

用yield可以简单的将一个函数改写成generator获得迭代能力，比起用类的实例保存状态计算下一个next()的值，不仅仅代码简洁，而且执行流程非常清晰



## yield用于文件读取
直接对文件对象调用read()方法，会导致不可预测的内存占有，好的方法是利用固定长度的缓冲区不断读取文件的内容。通过yield，我们不需要编写读文件的迭代类，就可以轻松读取文件：

def read_file(fpath):

      BLOCK_SIZE =1024

      with open(fpath,'rb') as f:

           while True:

                block = f.read(BLOCK_SIZE)

                if block:

                      yield block

                else 

                    return


