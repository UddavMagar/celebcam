# # from django.contrib import admin
# from django.urls import path
# from .import views

# urlpatterns = [
#     # path('admin/', admin.site.urls),
#     # path('',views.login,name="login"),
#     path('',views.register,name="register"),
#     path('register_fun',views.register_fun,name="register"),
#     # path('login',views.login,name="login")
    
# ]
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^login/register/$',views.register_fun, name='register'),
    url(r'^login/$',views.login_fun, name='login'),
    url(r'^logout/$',views.logout_fun, name='logout'),
    url(r'^online/$', views.online, name='online'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^messages/$', views.messages, name='messages'),
    url(r'^$', views.homepage, name='homepage'),
    url(r'^detail/$', views.Celibritydetail, name='celibritydetail'),
    url(r'^celibrity/$', views.celibrityhome, name='celibrityhome'),
    url(r'^service/$', views.request_services, name='service'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^download/$', views.download, name='download'),
    url(r'^notification/$', views.notification, name='notification'),
    url(r'^chattime/$', views.chattime, name='chattime'),
    url(r'^comment/$', views.comment, name='comment'),
]

