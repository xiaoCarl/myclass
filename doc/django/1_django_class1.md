1_django_class1.md

#创建第一个django项目

## STEP1:下载django
    
   $sudo pip3 install django

## STEP2:创建第一个django项目 myproject

   $django-admin   startproject myproject


以上命令自动生成的项目文件结构：
    
    $cd myproject
    $tree
    .
    ├── manage.py
    └── myproject
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py

    1 directory, 5 files


* django-admin是用于管理Django的命令行工具集
* manage.py是每个Django项目中自动生成，管理本项目的命令行集 

## STEP3:给自己的项目增加第一个应用app1

    $ python manage.py startapp app1
    $ tree
    .
    ├── app1
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    ├── manage.py
    └── myproject
        ├── __init__.py
        ├── __init__.pyc
        ├── settings.py
        ├── settings.pyc
        ├── urls.py
        └── wsgi.py

    3 directories, 14 files

## STEP4: 数据库的迁移(可选)
   
    $python manage.py migrate


    Operations to perform:
      Apply all migrations: admin, auth, contenttypes, sessions
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying auth.0008_alter_user_username_max_length... OK
      Applying sessions.0001_initial... OK

## STEP5: 修改setting.py文件

### 在INSTALLED_APPS中配置app
    INSTALLED_APPS = [
    'app1',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]

### 在ALLOWED_HOSTS配置外部访问用的HostIP地址

    ALLOWED_HOSTS = [u'10.43.177.78']  #如配置外部访问地址'10.43.177.78'


## STEP6: 启动系统,myproject项目作为一个WEB Server
    
    $python manage.py runserver


terminal下执行"python manage.py runserver"这样执行默认的路径是127.0.0.1:8000
指定端口或地址就再后面写上，如："python manage.py runserver 127.0.0.1:8888"


## 其他一些常用的命令：

* 检查整个项目

    django-admin check

* 对单个app检查,如检查app1

    python manage.py check app1

* 自动进入setting.py设置数据库

    python manage.py dbshell

* 进入python解释窗口    
    
    python manage.py shell

* 创建超级管理员

    python manage.py createsuperuser
