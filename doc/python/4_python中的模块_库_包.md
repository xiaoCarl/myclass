# python中的模块、库、包


## 1.python模块是：
python模块：包含并且有组织的代码片段为模块。

表现形式为：写的代码保存为文件。这个文件就是一个模块。sample.py 其中文件名smaple为模块名字。

关系图：

![Alt text](./image/python4_1.jpg)


## 2.python包是：
包是一个有层次的文件目录结构，它定义了由n个模块或n个子包组成的python应用程序执行环境。通俗一点：包是一个包含__init__.py 文件的目录，该目录下一定得有这个__init__.py文件和其它模块或子包。

常见问题：

引入某一特定路径下的模块

使用sys.path.append(yourmodulepath)

将一个路径加入到python系统路径下，避免每次通过代码指定路径

利用系统环境变量 export PYTHONPATH=$PYTHONPATH:yourmodulepath，

直接将这个路径链接到类似/Library/Python/2.7/site-packages目录下

好的建议：

经常使用if __name__ == '__main__'，保证写包既可以import又可以独立运行，用于test。

多次import不会多次执行模块，只会执行一次。可以使用reload来强制运行模块，但不提倡。

常见的包结构如下：                 

package_a├── __init__.py

                 ├── module_a1.py

                 └── module_a2.py

package_b├── __init__.py

                 ├── module_b1.py 

                 └── module_b2.py

main.py

如果main.py想要引用package_a中的模块module_a1，可以使用:

from package_a import module_a1

import package_a.module_a1

如果packagea中的module_a1需要引用package_b，那么默认情况下，python是找不到package_b。我们可以使用sys.path.append('../'),可以在package_a中的__init__.py添加这句话，然后该包下得所有module都添加* import __init_即可。

关系图：


![Alt text](./image/python4_2.jpg)


## 3.库（library）
库的概念是具有相关功能模块的集合。这也是Python的一大特色之一，即具有强大的标准库、第三方库以及自定义模块。
