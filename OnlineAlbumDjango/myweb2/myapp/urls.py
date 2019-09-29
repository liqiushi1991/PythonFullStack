from django.conf.urls import url
from . import views

urlpatterns = [
	#当前应用的主入口视图
    url(r'^$', views.index,name="index"),

    #HttpResponse实例路由
    url(r'^rp/(?P<cn>[a-z])$',views.rpdemo,name="rpdemo"),

    #HttpRequest实例路由
    url(r'^rq$',views.rqdemo,name="rqdemo"),

    #验证码
    url(r'^verifycode$',views.verifycode,name="verifycode"),
]
