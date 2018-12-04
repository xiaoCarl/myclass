
# python的namespace和scope （命名空间和作用域）

## namespace
1、python中的namespace 是名称(标识符)到对象的映射。

具体来说，python为模块、函数、类、对象保存一个字典(__dict__)，里面就是重名称到对象的映射。



2、在面向对象编程中，python与C++最大的差别之一就在于python中的namespace是可以动态变化的，类的成员，类实例的成员都可以动态添加，所做的不过是在相应的namespace字典中添加一项。

这里特别指出的函数（成员函数或全局函数）也有自己的namespace字典，甚至可以动态添加



3、Namespace（只）是 从名字到对象的一个映射(a mapping from name to objects) 。大部分namespace都是按Python中的字典来实现的。

 有一些常见的namespace：built-in中的集合（ abs() 函数等）、一个模块中的全局变量等。

从某种意义上来说，一个对象(object)的所有属性(attribute)也构成了一个namespace。在程序执行期间，可能（其实是肯定）会有多个名空间同时存在。不同namespace的创建/销毁时间也不同。

此外，两个不同namespace中的两个相同名字的变量之间没有任何联系。





## scope


有了namespace基础之后，让我们再来看看scope。Scope是Python程序的一块文本区域(textual region)。

在该文本区域中，对namespace是可以直接访问，而不需要通过属性来访问。

Scope是定义程序该如何搜索确切地“名字-对象”的名空间的层级关系。
(The “scope” in Python defines the “hirerchy level” in which we search namespaces for
certain “name-to-object” mappings.)



### Tip1:

直接访问：对一个变量名的引用会在所有namespace中查找该变量，而不是通过属性访问。

属性访问：所有名字后加 . 的都认为是属性访问。

如 module_name.func_name ，需要指定 func_name 的名空间，属于属性访问。
而 abs(-1) ， abs 属于直接访问。



### Tip2:

对于变量的作用域查找有了了解之后，还有两条很重要的规则：

Important

赋值语句通常隐式地会创建一个局部(local)变量，即便该变量名已存在于赋值语句发生的上一层作用域中；
如果没有 global 关键字声明变量，对一个变量的赋值总是认为该变量存在于最内层(innermost)的作用域中；

### Tip3:

其实只要在编程的时候注意一下，不要使用相同的标识符，基本上就可以避免任何与命名空间相关的问题。

还有就是在一个函数中尽量不要使用上层命名空间中的标识符，如果一定要用，也最好使用参数传递的方式进行，这样有利于保持函数的独立性。

两者之间有什么联系呢？
Important

在Python中，scope是由namespace按特定的层级结构组合起来的。

scope一定是namespace，但namespace不一定是scope.

## LEGB-rule
在一个Python程序运行中，至少有4个scopes是存在的。

直接访问一个变量可能在这四个namespace中逐一搜索。

Local(innermost)包含局部变量。比如一个函数/方法内部。

Enclosing包含了非局部(non-local)也非全局(non-global)的变量。比如两个嵌套函数，内层函数可能搜索外层函数的namespace，但该namespace对内层函数而言既非局部也非全局。 

Global(next-to-last)当前脚本的最外层。比如当前模块的全局变量。 

Built-in(outtermost)Python __builtin__ 模块。包含了内建的变量/关键字等。 

那么，这么多的作用域，Python是按什么顺序搜索对应作用域的呢？

著名的”LEGB-rule”，即scope的搜索顺序：

Important

Local -> Enclosing -> Global -> Built-in

怎么个意思呢？

当有一个变量在 local 域中找不到时，Python会找上一层的作用域，即 enclosing 域（该域不一定存在）。enclosing 域还找不到的时候，再往上一层，搜索模块内的 global 域。最后，会在 built-in 域中搜索。对于最终没有搜索到时，Python会抛出一个 NameError 异常。

作用域可以嵌套。比如模块导入时。

这也是为什么不推荐使用 from a_module import * 的原因，导入的变量可能被当前模块覆盖。









变量作用域（scope）在Python中是一个容易掉坑的地方。



python命名空间namespace和作用域
Python的变量定义后都有自己的作用域，每个作用域内都有名字空间。注意⚠️，python所有的变量和函数都是先定义，后使用！！

名称空间就是变量名称与对象的关联关系。Python中使用变量名引用对象，需要使用该变量时，就在命名空间中进行搜索，获取对应的对象。直接访问一个变量，会在四个namespace中逐一搜索，即：Local(innermost)、Enclosing、Global(next-to-last)、Built-in(outtermost)。

1、Local(innermost)：局部变量，函数内部的变量

2、Enclosing：也是局部变量，闭包函数变量。

3、 Global：全局变量，脚本文件无缩进的变量。

4、Built-in(outtermost)：Python内置的变量和关键词

python使用的搜索顺序是：1-2-3-4 

Local -> Enclosing -> Global -> Built-in
每个函数都有着自已的名称空间，叫做局部名称空间；

每个局部名称空间的外部的名称空间，叫做封闭区域；如内嵌函数的外部函数的局部名称空间，就是这个内嵌函数的封闭区域。

每个模块拥有它自已的名称空间，叫做全局名称空间；

还有就是内置名称空间，任何模块均可访问它，它存放着内置的函数和异常。

python运行机制：

当有一个变量在 local 域中找不到时，Python会找上一层的作用域，即 enclosing 域（该域不一定存在）。
enclosing 域还找不到的时候，再往上一层，搜索模块内的 global 域。最后，会在 built-in 域中搜索。
对于最终没有搜索到时，Python会抛出一个 NameError 异常。



Python除了def/class/lambda 外，其他如: if/elif/else/  try/except  for/while并不能改变其作用域。定义在他们之内的变量，外部还是可以访问。

globals() 和 locals() 提供了基于字典的访问全局和局部变量的方式
