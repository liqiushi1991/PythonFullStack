from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,name="index"),

    #模板语法测试路由
    url(r'^demo1$', views.demo1,name="demo1"),

    #模板继承测试路由
    url(r'^demo2$', views.demo2,name="demo2"),

    # 城市级联操作
    url(r'^showdistrict$', views.showdistrict, name='showdistrict'), #加载网页
    url(r'^district/([0-9]+)$', views.district, name='district'),  #Ajax加载城市信息

]