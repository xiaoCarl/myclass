# shell基本语法

1、打印输出
 a)  echo hello world!

 b)  echo "hello world!“

 c)

   myvar="hello world!"

   echo $myvar

2、变量
$myvar

3、读取变量
echo  enter myvar:

read myvar

4、条件语句
如检查一个文件myfile.c是否存在

if [ -f myfile.c ]

then

。。。

fi

或者:

if [ -f myfile.c ] ;   then

。。。

fi

或者

if  test -f myfile.c

then

。。。

fi

5、for语句
for var in values

do

   statements

done



6、shell函数
function_name () ｛

  statements

}

如：

foo() {

echo "hello world!"

}


