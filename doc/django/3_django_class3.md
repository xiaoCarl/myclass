# Django静态文件的处理

模版页面的一般依赖一些静态文件（JS，CSS，Image等等）,下面是配置静态img文件的步骤

参考1：[Django 静态文件的处理](https://segmentfault.com/a/1190000004232816)


## STEP1 创建静态文件的目录static,将静态文件拷贝到该目录

	$mkdir static
	$cd static
    ...

	$tree
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
	├── db.sqlite3
	├── manage.py
	├── myproject
	│   ├── __init__.py
	│   ├── settings.py
	│   ├── urls.py
	│   └── wsgi.py
	├── static
	│   └── images
	│       └── demo.img
	└── templates
	    └── main.html
 
 ## STEP2 修改setting文件，在 STATIC_URL = '/static/' 下面增加以下内容：

	HERE = os.path.dirname(os.path.abspath(__file__))
	HERE = os.path.join(HERE, '../')
	STATICFILES_DIRS = (
	    # Put strings here, like "/home/html/static" or "C:/www/django/static".
	    # Always use forward slashes, even on Windows.
	    # Don't forget to use absolute paths, not relative paths.
	    os.path.join(HERE, 'static/'),
	)

## STEP3 配置静态文件的url路由(myproject/urls.py)

    from . import settings
    from django.conf.urls.static import static


    #在urls.py文件的最下面增加下面这些文件
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
