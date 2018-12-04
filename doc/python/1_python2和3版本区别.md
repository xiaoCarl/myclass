1、Python3没有考虑向下兼容

2、python3的变化主要是与喜爱几个方面：

print函数：
Python3不支持print语句，取而代之的是print（）函数

2.x:

print "fish"

3.x

print("fish")

Unicode:
3.x源码文件默认使用utf-8编码

2.x 有ASCLL str类型， uncode()是单独的，不是byte类似

3.x有字节类： byte和bytearrarys

除法：
2.x

1/2=0

1.0/2.0=0.5

3.x

1/2 =0.5

异常处理


由except exc,var 改为except exc as var ,    3,x使用as作为关键字





不等运算符
2.x  不等于有两种写法 != 和<>

3.x  中去掉了<>



从键盘录入字符串
2.x    raw_input("提示信息）输入默认字符串类型返回字符串类型，input() 输入数字，返回数字类型（int,float)

3.x   input("提示信息”） 输入默认字符串类型，返回字符串类型



map、filter和reduce


mao和filter内置函数，编变成了类，返回结果也从当初的列表变成了一个可迭代的对象

reduce不属于内置模块，已经移到functools模块当中

默认路径的处理
3.x增加了pathlib的默认模块，帮助大家避免使用os.path.joins
