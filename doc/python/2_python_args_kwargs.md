当函数的参数不确定的时候，可以使用*args和**kwargs;

*args 没有key值， **kwargs 有key值



*args可以看成可以容纳多个变量组成的list

**kwargs 可以看成容纳多个key和value的dictionary


>>> def func1(arg, *args):    #  *args就是多个不定参数的列表 
...         print "arg:", arg 
...         for i in args: 
...                 print " other arg:",i 
... 
>>> func1(1,2,"abcd") 
arg: 1
other arg: 2
other arg: abcd
>>>

>>> def func2(arg,**kwargs):   # **kwargs就是带关键字的不定参数 
...          for i in kwargs: 
...                 print "key:%s,arg:%s" %(i, kwargs[i]) 
... 
>>> func2(1,myarg1=2,myarg2='aaaa') 
key:myarg1,arg:2
key:myarg2,arg:aaaa
>>>



如果在函数中调用*或者**参数，表示将字段扩展为关键字参数：

如

arg=(1,2,3)

func(*arg)  等价于 func(1,2,3)



dictpara={'a':1,'b':2}

func(**dictpara) 等价于 func(a=1,b=2)


