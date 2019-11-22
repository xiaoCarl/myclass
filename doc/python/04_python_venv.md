# 用virtualenv建立多个Python独立开发环境

同的人喜欢用不同的方式建立各自的开发环境，但在几乎所有的编程社区，总有一个（或一个以上）开发环境让人更容易接受。 使用不同的开发环境虽然没有什么错误，但有些环境设置更容易进行便利的测试，并做一些重复/模板化的任务，使得在每天的日常工作简单并易于维护。

## 什么是virtualenv？
在Python的开发环境的最常用的方法是使用 virtualenv 包。 Virtualenv是一个用来创建独立的Python环境的包。现在，出现了这样的问题：为什么我们需一个独立的Python环境？ 要回答这个问题，请允许我引用virtualenv自己的文档：

virtualenv is a tool to create isolated Python environments.

The basic problem being addressed is one of dependencies and versions, and indirectly permissions. Imagine you have an application that needs version 1 of LibFoo, but another application requires version 2. How can you use both these applications? If you install everything into /usr/lib/python2.7/site-packages (or whatever your platform’s standard location is), it’s easy to end up in a situation where you unintentionally upgrade an application that shouldn’t be upgraded.

Or more generally, what if you want to install an application and leave it be? If an application works, any change in its libraries or the versions of those libraries can break the application.

Also, what if you can’t install packages into the global site-packages directory? For instance, on a shared host.

In all these cases, virtualenv can help you. It creates an environment that has its own installation directories, that doesn’t share libraries with other virtualenv environments (and optionally doesn’t access the globally installed libraries either).

我们需要处理的基本问题是包的依赖、版本和间接权限问题。想象一下，你有两个应用，一个应用需要libfoo的版本1，而另一应用需要版本2。如何才能同时使用这些应用程序？如果您安装到的/usr/lib/python2.7/site-packages（或任何平台的标准位置）的一切，在这种情况下，您可能会不小心升级不应该升级的应用程序。

简单地说，你可以为每个项目建立不同的/独立的Python环境，你将为每个项目安装所有需要的软件包到它们各自独立的环境中。

安装与使用virtualenv
安装 virtualenv 很简单：

pip install virtualenv 
virtualenv安装完毕后，可以通过运行下面的命令来为你的项目创建独立的python环境：

mkdir nowamagic_venv
virtualenv --distribute nowamagic_venv
OK，成功。上面发生了什么？你创建了文件夹 nowamagic_venv 来存储你的新的独立Python环境。 这个文件夹位于 /root 下面。

我们再来看看输出：

New python executable in nowamagic_venv/bin/python2.7
Also creating executable in nowamagic_venv/bin/python
Installing Setuptools......done.
Installing Pip...........done.
--distribute 选项使virtualenv使用新的基于发行版的包管理系统而不是 setuptools 获得的包。 你现在需要知道的就是 --distribute 选项会自动在新的
虚拟环境中安装 pip ，这样就不需要手动安装了。 当你成为一个更有经验的Python开发者，你就会明白其中细节。

  activate：这个virtualenv的激活文件
  pip：这个virtualenv的独立pip
  python：python解释器的一个副本
  lib/python2.7：所有的新包会被存在这


## 试验一下

通过下面的命令激活这个virtualenv：

[root@nowamagic ~]# cd nowamagic_venv
[root@nowamagic nowamagic_venv]# source bin/activate
(nowamagic_venv)[root@nowamagic nowamagic_venv]#

运行下面的命令可以更好地理解两者的差异，如果已经进入virtualenv请先离开。

deactivate  #离开

首先让我们看看如果调用python/pip命令它会调用那一个。

[root@nowamagic ~]# which python
/usr/bin/python
[root@nowamagic ~]# which pip
/usr/local/bin/pip

再来一次！这次打开virtualenv，然后看看有什么不同。我的机子上显示如下：

[root@nowamagic ~]# which python
/root/nowamagic_venv/bin/python
[root@nowamagic ~]# which pip
/root/nowamagic_venv/bin/pip
virtualenv拷贝了Python可执行文件的副本，并创建一些有用的脚本和安装了项目需要的软件包，你可以在项目的整个生命周期中安装/升级/删除这些包。 它也修改了一些搜索路径，例如PYTHONPATH，以确保：

当安装包时，它们被安装在当前活动的virtualenv里，而不是系统范围内的Python路径。
当import代码时，virtualenv将优先采取本环境中安装的包，而不是系统Python目录中安装的包。
还有一点比较重要，在默认情况下，所有安装在系统范围内的包对于virtualenv是可见的。 这意味着如果你将simplejson安装在您的系统Python目录中，它会自动提供给所有的virtualenvs使用。 这种行为可以被更改，在创建virtualenv时增加 --no-site-packages 选项的virtualenv就不会读取系统包，如下：

virtualenv nowamagic_venv --no-site-packages





