from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Photos
from datetime import datetime
import time
from PIL import Image
from django.core.paginator import Paginator
import os
from myweb.settings import BASE_DIR

# Create your views here.


def index(request):
    # return HttpResponse("Hello")
    return render(request, "myapp/index.html")


def indexPhotos(request, pIndex=1):
    # return HttpResponse("show Users...")
    # 获取相册信息
    p_list = Photos.objects.all()
    p = Paginator(p_list, 4)

    if pIndex == "":
        pIndex = 1

    p_list2 = p.page(pIndex)
    plist = p.page_range
    context = {"ulist": p_list2, "plist": plist, "pIndex": int(pIndex)}

    return render(request, "myapp/photos/index.html", context)


def addPhotos(request):
    return render(request, "myapp/photos/add.html")


def delPhotos(request, pid):
    try:
        # return HttpResponse("id"+uid)
        ob = Photos.objects.get(id=pid)
        photo_name = ob.photo_name
        ob.delete()
        try:
            os.remove(os.path.join(BASE_DIR, 'static/pics/' + photo_name))
            os.remove(os.path.join(BASE_DIR, 'static/pics/s_' + photo_name))
            context = {"info": "数据及图片删除成功！"}

        except:
            context = {"info": "数据删除成功！"}

    except:
        context = {"info": "删除失败！"}
    return render(request, "myapp/photos/info.html", context)


def editPhotos(request, pid):
    try:
        ob = Photos.objects.get(id=pid)
        photo_name = ob.photo_name
        try:
            os.remove(os.path.join(BASE_DIR, 'static/pics/' + photo_name))
            os.remove(os.path.join(BASE_DIR, 'static/pics/s_' + photo_name))

        except:
            print("未能找到图片")
        context={"photo": ob}
        return render(request,"myapp/photos/edit.html", context)
    except Exception as err:
        print(err)
        context = {"info": "没有找到要修改的信息！"}
        return render(request, "myapp/photos/info.html", context)


def updatePhotos(request, pid):
    '''执行图片的上传'''
    myfile = request.FILES.get("photo_name", None)
    print(myfile)
    if not myfile:
        return HttpResponse("没有上传文件信息")
    filename = str(time.time())+"."+myfile.name.split('.').pop()
    destination = open("./static/pics/"+filename,"wb+")
    for chunk in myfile.chunks():      # 分块写入文件
        destination.write(chunk)
    destination.close()

    # 执行图片缩放
    im = Image.open("./static/pics/"+filename)
    # 缩放到75*75(缩放后的宽高比例不变):
    im.thumbnail((75, 75))
    # 把缩放后的图像用jpeg格式保存:
    im.save("./static/pics/s_"+filename, None)

    try:
        photo = Photos.objects.get(id=pid)
        photo.title = request.POST['title']
        photo.photo_name = filename
        photo.addtime = datetime.now()
        photo.save()
        context = {"info": "修改成功！"}
    except Exception as err:
        print(err)
        context = {"info": "修改失败！"}
    return render(request, "myapp/photos/info.html", context)

@csrf_exempt
def upload(request):
    '''执行图片的上传'''
    myfile = request.FILES.get("photo_name", None)
    print(myfile)
    if not myfile:
        return HttpResponse("没有上传文件信息")
    filename = str(time.time())+"."+myfile.name.split('.').pop()
    destination = open("./static/pics/"+filename,"wb+")
    for chunk in myfile.chunks():      # 分块写入文件
        destination.write(chunk)
    destination.close()

    # 执行图片缩放
    im = Image.open("./static/pics/"+filename)
    # 缩放到75*75(缩放后的宽高比例不变):
    im.thumbnail((75, 75))
    # 把缩放后的图像用jpeg格式保存:
    im.save("./static/pics/s_"+filename, None)

    try:
        photo = Photos()
        photo.title = request.POST['title']
        photo.photo_name = filename
        photo.addtime = datetime.now()
        photo.save()
        context = {"info": "添加成功！"}
    except Exception as err:
        print(err)
        context = {"info": "添加失败！"}
    return render(request, "myapp/photos/info.html", context)
