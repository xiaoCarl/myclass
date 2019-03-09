# 使用Django Channels的方式实现websocket通信

Django Channels的官方文档路径：

[channels的官方文档](https://channels.readthedocs.io/en/latest/)


## STEP1:安装channels包

    sudo pip3 install channels

## STEP2:编辑setting.py文件，

### 增加'channels'到 'INSTALLED_APPS'

	INSTALLED_APPS = [
	    'channels',
	    'app1',
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	]

### 在setting文件底部增加以下内容：

	# Channels
    ASGI_APPLICATION = 'myproject.routing.application'

## STEP3: 在app1中增加一个新文件consumers.py,在文件中添加如下内容：

	from channels.generic.websocket import WebsocketConsumer
	import json

	class ChessConsumer(WebsocketConsumer):
	    def connect(self):
	        self.accept()

	    def disconnect(self, close_code):
	        pass

	    def receive(self, text_data):
	        text_data_json = json.loads(text_data)
	        message = text_data_json['message']

	        self.send(text_data=json.dumps({
	            'message': message
	        }))

## SETP4：在app1目录下增加新文件routing.py

	from django.conf.urls import url

	from . import consumers

	websocket_urlpatterns = [
	    url(r'playchess/$', consumers.ChessConsumer),
	]

## SETP4:在myproject目录下增加新文件routing.py
	
	from channels.auth import AuthMiddlewareStack
	from channels.routing import ProtocolTypeRouter, URLRouter
	import app1.routing

	application = ProtocolTypeRouter({
	    # (http->django views is added by default)
	    'websocket': AuthMiddlewareStack(
	        URLRouter(
	            app1.routing.websocket_urlpatterns
	        )
	    ),
	})

## STEP5:修改main.html模版中websocket建链请求路径

    ws_chess= new WebSocket('ws://' + window.location.host +'/playchess/');

## SETP6: 运行服务器
    $ python3 manage.py runserver  

## STEP7：在浏览器里访问 "http://127.0.0.1:8000/main"

   可以发起websocket建链，进行消息互发

