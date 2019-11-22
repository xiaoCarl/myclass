# 装饰器


## 装饰器本质上是一个函数


装饰器通常用于在不改变原有函数代码和功能的情况下，为其添加额外的功能。比如在原函数执行前先执行点什么，在执行后执行点什么。



装饰器是一个很著名的设计模式，经常被用于有切面需求的场景，较为经典的有插入日志、性能测试、事务处理等。装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量函数中与函数功能本身无关的雷同代码并继续重用。概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能。



装饰器是一个函数,一个用来包装函数的函数，装饰器在函数申明完成的时候被调用，调用之后返回一个修改之后的函数对象，将其重新赋值原来的标识符，并永久丧失对原始函数对象的访问(申明的函数被换成一个被装饰器装饰过后的函数)

当我们对某个方法应用了装饰方法后， 其实就改变了被装饰函数名称所引用的函数代码块入口点，使其重新指向了由装饰方法所返回的函数入口点。

由此我们可以用decorator改变某个原有函数的功能，添加各种操作，或者完全改变原有实现

## 分类：

装饰器分为无参数decorator，有参数decorator

* 无参数decorator

生成一个新的装饰器函数

* 有参decorator

有参装饰，装饰函数先处理参数，再生成一个新的装饰器函数，然后对函数进行装饰
装饰器有参/无参，函数有参/无参，组合共4种

具体定义：
decorator方法

A.把要装饰的方法作为输入参数，

B.在函数体内可以进行任意的操作(可以想象其中蕴含的威力强大，会有很多应用场景)，

C.只要确保最后返回一个可执行的函数即可（可以是原来的输入参数函数， 或者是一个新函数）

无参数装饰器 – 包装无参数函数
不需要针对参数进行处理和优化

def decorator(func):
    print "hello"
    return func

@decorator
def foo():
    pass

foo()


foo()等价于:

foo = decorator(foo)
foo()

无参数装饰器 – 包装带参数函数
def decorator_func_args(func):
    def handle_args(*args, **kwargs): #处理传入函数的参数
        print "begin"
        func(*args, **kwargs)   #函数调用
        print "end"
    return handle_args


@decorator_func_args
def foo2(a, b=2):
    print a, b

foo2(1)
foo2(1)等价于

foo2 = decorator_func_args(foo2)
foo2(1)

带参数装饰器 – 包装无参数函数
def decorator_with_params(arg_of_decorator):#这里是装饰器的参数
    print arg_of_decorator
    #最终被返回的函数
    def newDecorator(func): 
        print func
        return func
    return newDecorator


@decorator_with_params("deco_args")
def foo3():
    pass
foo3()

与前面的不同在于：比上一层多了一层封装，先传递参数，再传递函数名

第一个函数decomaker是装饰函数，它的参数是用来加强“加强装饰”的。由于此函数并非被装饰的函数对象，所以在内部必须至少创建一个接受被装饰函数的函数，然后返回这个对象（实际上此时foo3= decorator_with_params(arg_of_decorator)(foo3)）

带参数装饰器– 包装带参数函数
def decorator_whith_params_and_func_args(arg_of_decorator):
    def handle_func(func):
        def handle_args(*args, **kwargs):
            print "begin"
            func(*args, **kwargs)
            print "end"
            print arg_of_decorator, func, args,kwargs
        return handle_args
    return handle_func


@decorator_whith_params_and_func_args("123")
def foo4(a, b=2):
    print "Content"

