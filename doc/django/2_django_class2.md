# 编写一个"hello world"网页

## STEP1 在 app1/view.py文件里,增加以下代码

    from django.shortcuts import HttpResponse       #导入HttpResponse模块
 
    def index(request):               #request是必须带的实例。类似class下方法必须带self一样
        return HttpResponse("Hello World!!")   #通过HttpResponse模块直接返回字符串到前端页面
 
## STEP2 配置url路由(myproject/urls.py)

    from app1 import views              #导入views模块
    from django.conf.urls import url
 
    urlpatterns=[
        url(r'^index/',views.index)     #配置当访问index/时去调用views下的index方法

## STEP3 运行server

    $ python manage.py runserver

## STEP4 在浏览器里访问 "http://127.0.0.1:8000/index"    

# 返回一个使用模版的网页，模版名称为"main.html"

## STEP1 创建一个templates目录，存放main.html文件

	$ mkdir templates
	$ tree
	.
	├── app1
	│   ├── admin.py
	│   ├── apps.py
	│   ├── __init__.py
	│   ├── migrations
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
	└── templates

## STEP2 在 app1/view.py文件里,增加以下代码
   
    from django.shortcuts import render     #导入render模块

    def show_main(request):
        return render(request,'main.html')   #返回

## STEP3 配置url路由(myproject/urls.py)
    
    from app1 import views 

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^main/', views.show_main),
    ]
      
## STEP4 修改setting文件，在 TEMPLATES 字段中增加模版对应的路径

	TEMPLATES = [
	    {
	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
	        'DIRS': [os.path.join(BASE_DIR,'app1/templates')], #指向模版存放的路径
	        'APP_DIRS': True,
	        'OPTIONS': {
	            'context_processors': [
	                'django.template.context_processors.debug',
	                'django.template.context_processors.request',
	                'django.contrib.auth.context_processors.auth',
	                'django.contrib.messages.context_processors.messages',
	            ],
	        },
	    },
	]

## STEP5 运行server

    $ python manage.py runserver

## STEP6 在浏览器里访问 "http://127.0.0.1:8000/main"    
	


