# python vs java

* Python和Java是两种截然不同的编程语言，但两者对于现在的程序员来说都是十分有用的工具。如果你刚开始考虑学习编程，你可能会发现Python更加易学。Pyton的语法设计的非常直观，并且其相对的简单性让新手们可以快速上手写各种应用。而Java的学习曲线则更加陡峭，它非常适用于开发在各种平台上都可以运行的应用。

* Dynamic vs Static Typing 动态类型 vs 静态类型
Python与Java之间最大的区别之一就是两种语言处理变量的方式。Java强迫你在第一次声明变量时定义其类型并且不允许你在后面的程序中更改它的类型。这就是所谓的静态类型。与之相对，Python使用的是动态类型，允许你改变一个变量的类型，例如可以把整型替换为字符串。

例如在Java中声明变量：

    int var = 0;

我们需要先确定变量的类型，再为变量赋值。而在Python中，变量无需事先声明：
    
    var = 0

备注：python3.5版本开始，增加了函数类型注解，python3.6增加了变量类型注解，类型注解会极大的方便大型项目使用。
函数类型注解:
    
    def add(x:int, y:int) -> int:
        return x+y

变量类型注解:    

    var1: int = 123
    var2: str = 'hello'

更进一步，如果你需要指明一个全部由整数组成的列表：
    
    from typing import List
    l: List[int] = [1, 2, 3]

* Braces vs Indentation 括号 vs 缩进
Python与众多编程语言的不同之处还在于它使用缩进将代码分割成块。Java，像大部分其他语言一样，使用大括号定义函数和类定义的开头和结尾。使用缩进的好处在于它强迫你将你的程序写得比较易读，不会有缺括号导致错误的可能。

* 分号 vs 换行 
Java中语句的结束强制以";"为结尾，Python中我们当然也可以用分号，但并不建议这样用。通常在Python中我们用换行表示语句的结束。

## 基本变量类型
* Java:我们常说的八大基本类型：byte,short,int,long,float,double,char,boolean。除此之外还有String,List,Map
* Python:五个标准的数据类型：Number,String,List,Tuple,Dictionary 其中Number包括int,long,float,complex

## 数
* python有四种数据：int整数，long长整数、float浮点数和complex复数
* java有char，short,byte，int，long，float,double类型

## 字符串
1.字符串表示
* Python中没有表示单个常量字符串类型的char类型，其可以用单引号‘ ’或双引号“ ”来表示一个字符串，也可以用三引号来表示一个多行字符串
* Java中char表示单个字符，String表示一个字符串，常量字符或字符串用双引号“ ”表示

2.多行字符串
* Python在字符串末尾加上反斜杠（/）表示字符串在下一行继续
* Java用加号（+）表示字符串在下一行继续

## 数组Array
参考C语言，数组大小是静态定义好的不能伸缩；数组中的元素类型要一致

Java定义参考：

    String[] myarr={"a","b","c"};  //定义了长度为3，有初始值的数组

或者
 
    String[] myarr=new String[5];  //定义了长度为5的数组

Python定义参考：

Python有两种方式提供数组的定义，引入数组定义主要是保证元素类型一致，numpy功能远远强标准库：

* 标准库array模块, 使用起来与List十分接近，但是存储的变量类型只能是一种，这个类型也便于python调用C语言的时候，进行相关数据结构的转换
* 使用numpy模块定义同种元素的多维数组，NumPy的数组类被称作ndarray，更多重要ndarray对象属性有：ndarray.ndim(数组轴的个数,秩);ndarray.shape(数组的维度);ndarray.dtype(数组中元素类型的对象,可以指定dtype使用标准Python类型,也可以NumPy提供它自己的数据类型)

备注：numpy可以用以下函数array, zeros, zeros_like, ones, ones_like, empty, empty_like, arange, linspace, rand, randn, fromfunction, fromfile等定义合适的多维数组。

    import array

    myarr = array.array('i')
    myarr.append(10)

或者：

    >> import numpy as np
    >> myarr1 = np.arange(6) # 1d array
    [0 1 2 3 4 5]
   
    >>myarr2= np.arange(12).reshape(4,3) # 2d array
    [[ 0 1 2]
    [ 3 4 5]
    [ 6 7 8]
    [ 9 10 11]]

## 列表List
自动扩展的数组，动态增加元素，在python中List元素类型是可以动态变化的，Python3.5后可以限制元素类型固定；

Java实现：
因为List为一个接口，不能初始化，只能通过实例化它的实现类来使用list集合;Java提供了多种List的实现类： 
* ArrayList() : 代表长度可以改变得数组。可以对元素进行随机的访问，向ArrayList()中插入与删除元素的速度慢。 
* LinkedList(): 在实现中采用链表数据结构。插入和删除速度快，访问速度慢。

Java定义参考：

    List<String> mylist = new ArrayList<String>(); //初始化list集合
    mylist.add("a"); //集合添加数据

或者：

    List<String> mylist=new ArrayList<String>(){
        { add("a"); add("b");}
    };

Python定义参考：

    mylist = []
    mylist.append("a")
    mylist.append("b")

或者

    mylist = ["a","b"]  

备注：从python3.5 如果限定List元素类型，可以使用标注库typing.List定义

    from typing import List

    mylist: List[str] = ["a", "b"]

## 集合Set
没有重复对象的集合，在集合中没有重复的元素 

* Java实现
Set接口主要有以下两个实现类：
Hashset：HashSet类按照哈希算法来存取集合中的对象，存取速度比较快 
Treeset：TreeSet类实现了SortedSet接口，能够对集合中的对象进行排序。

Java定义参考：

    Set myset=new HashSet();
    String s1=new String("hello"); //引用类型-对象，不能是基础数据类型
    String s2=s1;
    String s3=new String("world");
    myset.add(s1);
    myset.add(s2);
    myset.add(s3);
    System.out.println(set.size());//打印集合中对象的数目为 2。 

Python定义参考

    myset = set(['A', 'B', 'C'])
    myset.add('D')

## 映射（字典）Map（Dictionary）
是一种把键对象和值对象映射的集合，它的每一个元素都包含一对键对象和值对象。

* Java实现：
Java的Map接口类主要有以下实现类：HashMap,HashTable,TreeMap

Java定义参考：

    Map<String, String> mymap=new HashMap<String, String>();
    mymap.put("key1", "value1");
    mymap.put("key2", "value2");

或者

    Map<String, Object> mymap = new HashMap<String, Object>(){ 
        {put("key1", "value1");
        put("key2", "value2");
        put("key3", "value3");}
    };

Python定义参考:

    mydict={}
    mydict["key1"]="value1"
    mydict["key2"]="value2"

或者：

    mydict = { 'key1': "value1", 'key2': "value2", 'Bart': 59 }

## 元组Tuple

对于一个集合的数据希望只提供Readonly方式，不能修改。python提供元组类型Tuple；

使用场景：
* 不变集合Tuple是不可改变的，所以可以做Dict的关键字，Set的元素
* tuple 作为不可变类型性能上优于list，这只是一方面，更重要的是 tuple 可用于存储异构(heterogeneous)数据，可作为没有字段名的记录（record）来用.

比如用tuple来记录一个人的身高、体重、年龄:

    name, age, height, weight= ("zhangsan", 20, 180, 80)

而list一般用于存储同构数据(homogenous)，同构数据就是具有相同意义的数据;比如下面都是字符串类型，代表用户的名字

    ["zhangsan", "Lisi", "wangwu"]

可能有人要跳出来说 list 可以存储任何类型的数据，但是，你操作数据库的时候你不会把任何东西都往一个list塞吧。正确的方式应该是：

    [("zhangsan", 20, 180, 80), ("wangwu", 20, 180, 80)]

正因为tuple作为没有名字的记录来使用在某些场景有一定的局限性，所以又有了一个namedtuple类型的存在，namedtuple可以指定字段名了。

* Tuple不变，性能优于List； 可以多线程访问；

* tuple类型对于Python自身来说是非常重要的数据类型，比如说函数调用，实际上会将顺序传入的参数先组成一个tuple；多返回值也是靠返回一个tuple来实现的。因为太常用，所以需要一个更有效的数据结构来提高效率，一个不可变的tuple对象从实现上来说可以比list简单不少。再比如说code对象会记录自己的参数名称列表，free variable名称列表等等，这些如果用list，就可能被从外部修改，这样可能导致解释器崩溃；那就只能选择改成一个函数每次都返回一个新的列表，这样又很浪费。所以即使是从解释器自身实现的角度上来说引入这样一个不可变的序列类型也是很重要的。

Python定义参考:

    mytuple = (1,"abcd",[1,2,3])
    print(mytuple[0]) //输出： 1   


### Java元组的实现
* 元组在计算机领域有着特殊的意义，这个名字听起来似乎有些陌生， 平时在写代码也基本没什么应用场景， 然而， 出人意料的是， 元组跟程序设计密切相关， 可能有的同学不知道， 关系数据库中的「纪录」的另一个学术性的名称就是「元组」， 一条记录就是一个元组， 一个表就是一个关系， 纪录组成表， 元组生成关系， 这就是关系数据库的核心理念。
* 元组是关系数据库不可脱离的部份， 但是在程序设计中， 元组并不显得那么不可或缺。 有一些编程语言本身就自带元组的语法， 比如说python、F#、haskell、scala等，另一些更为流行的编程语言却不带元组语法， 如Java、JavaScript、c++、c#等。
* 元组并不像数组、对象那样是不可缺少的编程元素，但是， 使用它却能对编写代码带来很多的便利，尤其是当一个函数需要返回多个值的情况下。对于这种情况， 普遍的做法是定义一个对象，把函数需要返回的值作为对象的属性设置，然后把函数的返回值类型设为这个对象的类型， 函数直接返回这个对象就相当于返回多个值了。或者可以让这个函数返回一个map数据结构，具体的数据存在这个map里面。 然而， 这两种做法各有缺陷， 第一种方法虽然可靠， 然而代码会显的异常臃肿。需求本身很简单， 只要让函数返回多个值 ， 然而用这种方法却需要事先定义好一个类型， 然后再实例化，再设置实例属性， 最后返回， 这样做的编码效率也未免太低了些。 第二种方法虽然快捷，却不够安全， 在函数的内部或许知道map里存储着什么样的值， 然而在函数外部， 却只知道这个函数的返回值是一个map，至于map里面存有哪些值，是什么类型都是一无所知的， 在多人开发的项目中这种弊端尤其明显 ，可悲的是这种做法在一些动态类型的语言中是首选的方案，这也是动态类型语言被吐槽安全性、可读性差的根本原因之一。 因此， 解决这类问题最好的方案就是使用元组。
* 在语法本身支持元组的语言中， 元组是用括号表示的，如(int,bool,string)就是一个三元组类型， 它的值可以是(1,true,"abc")。 需要注意是的每一个元组类型都是唯一的， (int,bool)，(bool,int)，(string,double)虽然都是二元组， 然而它们却是不同的元组， 假如把这里的某一个元组作为函数的返回值， 在可读性和安全性方面虽然不如前面讲的第一种使用自定义类型的方案， 然而却比第二种使用map的方案要好的多， 至少使用元组能知道函数会返回几个值， 这些值又分别是什么类型， 而且它还有第二种使用map的方案编码简单快捷的优势。

* 另人遗憾的是， 像java、c++、c#之类行业内主流的编程语言都不内置元组这一项特性，要使用元组必须自行实现，所幸现在这些编程语言都支持泛型， 实现非内置元组也变的异常简单， 但是毕竟是非语言内置的语法元素，使用起来肯定不如原生元组来的便捷。

* 下面介绍一个第三方的Java元组库类库，名称叫做Javatuples，有自己的官方主页， github star数也有几百，在Java元组库领域差不多起着垄断的地位了。

Javatuples定义的元组最大长度为10， 其实我觉得10元组的元素数量已经是太多了， 基本上没有什么可读性可言了。 元组类的定义如下
    
    Unit<A> (1 element)
    Pair<A,B> (2 elements)
    Triplet<A,B,C> (3 elements)
    Quartet<A,B,C,D> (4 elements)
    Quintet<A,B,C,D,E> (5 elements)
    Sextet<A,B,C,D,E,F> (6 elements)
    Septet<A,B,C,D,E,F,G> (7 elements)
    Octet<A,B,C,D,E,F,G,H> (8 elements)
    Ennead<A,B,C,D,E,F,G,H,I> (9 elements)
    Decade<A,B,C,D,E,F,G,H,I,J> (10 elements)
 
这些原型类都是泛型类， 所以尖括号中的字母可以使用任意类型来代替。

Java定义参考：（下面是一个三元组）

    String str = "abcd";
    Integer integ = 1234;
    Double[] doubleArray = {10,400000,5};

    Triplet<String,Integer,Double[]> triplet = Triplet.with(str, integ, doubleArray); 
    
    String myStr = triplet.getValue0();
    Integer myInteg = triplet.getValue1();
    Double[] myDoubleArray = triplet.getValue2();