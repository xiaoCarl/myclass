 
#  configparser模块

ConfigParser模块在python中用来读取配置文件，配置文件的格式跟windows下的ini配置文件相似，可以包含一个或多个节(section), 每个节可以有多个参数（键=值）。使用的配置文件的好处就是不用在程序员写死，可以使程序更灵活。 

注意：在python 3 中ConfigParser模块名已更名为configparser


## configparser函数常用方法：

读取配置文件：
`
 read(filename) #读取配置文件，直接读取ini文件内容

 sections() #获取ini文件内所有的section，以列表形式返回['logging', 'mysql']
  
 options(sections) #获取指定sections下所有options ，以列表形式返回['host', 'port', 'user', 'password']
  
 items(sections) #获取指定section下所有的键值对，[('host', '127.0.0.1'), ('port', '3306'), ('user', 'root'), ('password', '123456')]
  
 get(section, option) #获取section中option的值，返回为string类型

 getint(section,option) 返回int
 
 getfloat(section, option)  返回float
 
 getboolean(section,option) 返回boolen

`

## 举例如下：

### 配置文件ini如下：(注意，也可以使用：替换=)
`
[logging]
level = 20
path =
server =

[mysql]
host=127.0.0.1
port=3306
user=root
password=123456

`

### 代码如下：

`
import configparser
from until.file_system import get_init_path

conf = configparser.ConfigParser()
file_path = get_init_path()
print('file_path :',file_path)
conf.read(file_path)

sections = conf.sections()
print('获取配置文件所有的section', sections)

options = conf.options('mysql')
print('获取指定section下所有option', options)


items = conf.items('mysql')
print('获取指定section下所有的键值对', items)


value = conf.get('mysql', 'host')
print('获取指定的section下的option', type(value), value)

`

### 运行结果如下：

file_path : /Users/xxx/Desktop/xxx/xxx/xxx.ini
获取配置文件所有的section ['logging', 'mysql']
获取指定section下所有option ['host', 'port', 'user', 'password']
获取指定section下所有的键值对 [('host', '127.0.0.1'), ('port', '3306'), ('user', 'root'), ('password', '123456')]
获取指定的section下的option <class 'str'> 127.0.0.1

## 综合使用方法：

`
import configparser
"""
读取配置文件信息
"""

class ConfigParser():

    config_dic = {}
    @classmethod
    def get_config(cls, sector, item):
        value = None
        try:
            value = cls.config_dic[sector][item]
        except KeyError:
            cf = configparser.ConfigParser()
            cf.read('settings.ini', encoding='utf8')  #注意setting.ini配置文件的路径
            value = cf.get(sector, item)
            cls.config_dic = value
        finally:
            return value


if __name__ == '__main__':
    con = ConfigParser()
    res = con.get_config('logging', 'level')
    print(res)

`



~

