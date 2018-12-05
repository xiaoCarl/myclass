# Python调试

python有自带的pdb库，可以实现简单的调试功能，基本命令与gdb类似，不过功能不会有gdb那么强大，pdb主要支持多断点设置（可条件设置），代码级单步调试，查看堆栈信息，代码查看。命令行启动目标程序，加上-m参数，这样调用myscript.py的话断点就是程序的执行第一行之前：



 python -m pdb myscript.py  



正常运行脚本后，到了pdb.set_trace()那就会定下来，就可以看到调试的提示符(Pdb)了

一些常用指令：    

1、h(elp) [comman]  #打印可用指令及帮助信息  

2、r(eturn)  #运行代码直到下一个断点或当前函数返回  

3、b(reak) [[filename:]lineno | function[, condition]]  #指定文件某行或函数体来设置断点    

4、l(ist) [first[, last]]  #查看指定代码段    

5、n(ext)  #执行下一行  

6、s(tep) #执行下一行，若为函数则进入函数体  

7、p  #打印某个变量  

8、a(rgs)  #打印当前函数的参数  

9、w(here)  #打印堆栈信息  

10、d(own)  #移至下层堆栈  

11、u(p)  #移至上层堆栈  

12、j(ump)  #跳转到指定行  

13、continue / c  #继续执行  

14、disable [bpnumber [bpnumber]] #失效断点  

15、enable[bpnumber [bpnumber]]  #启用断点  

16、cl(ear) [filename:lineno | bpnumber [bpnumber]] #删除断点  

17、q(uit)/exit  #中止调试并退出  


## python常见调试方法


1、查看包属性

>>> help(sys)



2、python调试



import pdb #导入调试包

pdb.set_trace()

n :单步调试

c :continue

s(step into)

bt(打印堆栈)

p :打印变量


一般在需要调试的文件加入下面代码即可

################

_DEBUG = True

...

if _DEBUG == True

　　import pdb

　　pdb.set_trace()

################



## Python远程调试

import remote_pdb
remote_pdb.RemotePdb(host='0.0.0.0', port=4444).set_trace() #host='0,0,0,0'指当前主机

telnet 10.43.177.241 4444   /*如当前主机对外访问的IP地址为10.43.177.241， 通过telnet访问该主机的指定调试端口
