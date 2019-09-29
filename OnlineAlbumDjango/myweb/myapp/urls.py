from django.conf.urls import url
from . import views

urlpatterns = [
    #首页
    url(r'^$',views.index, name="index"),

    #相册信息管理路由
    url(r'^photos/$', views.indexPhotos, name="photos"),
    url(r'^photos/(?P<pIndex>[0-9]+)$', views.indexPhotos, name="photos"), #浏览信息
    url(r'^photos/add$', views.addPhotos, name="addphotos"), #加载添加表单

    # 上传照片
    url(r'^photos/insert$', views.upload, name="insertphotos"),

    url(r'^photos/del/(?P<pid>[0-9]+)$', views.delPhotos, name="delphotos"), #删除信息
    url(r'^photos/edit/(?P<pid>[0-9]+)$', views.editPhotos, name="editphotos"), #加载修改信息
    url(r'^photos/update/(?P<pid>[0-9]+)$', views.updatePhotos, name="updatephotos"), #执行信息修改
]