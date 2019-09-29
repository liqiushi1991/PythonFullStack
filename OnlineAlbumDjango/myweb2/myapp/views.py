from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse,Http404,HttpResponseNotFound

def index(request):
	#return HttpResponse("ok!")
	return render(request,"myapp/index.html")

def rpdemo(request,cn):
	'''HttpResponse实例'''
	if cn=="a":
		return HttpResponse("直接返回数据信息")
	elif cn=="b":
		context = {"info":"通过模板返回数据"}
		return render(request,"myapp/rpdemo.html",context)
	elif cn=="c":
		return redirect(reverse("rpdemo",args=['a']))
	elif cn=="d":
		#return JsonResponse({"name":"zhangsan","age":22})
		data = [{"name":"zhangsan","age":22},{"name":"lisi","age":25}]
		return JsonResponse(data,safe=False)
	elif cn=="e":
		# 获取当前的 响应对象
		response = HttpResponse('cookie的设置')
		# 使用响应对象进行cookie的设置
		response.set_cookie('myname','zhangsan')
		# 返回响应对象
		return response

	elif cn=="f":
		# 读取
		a = request.COOKIES.get('myname',None)
		if a:
		    return HttpResponse('cookie的读取：'+a)
		else:
		    return HttpResponse('cookie不存在')
	else:
		# 直接返回一个404,没有去加载404的模板页面
		return HttpResponseNotFound('<h1>Page not found</h1>')

		# 可以直接返回一个status状态码
		#return HttpResponse(status=403)

		# 返回一个404的错误页面
		# Http404("Poll does not exist")

def rqdemo(request):
	'''HttpRequest实例'''
	print("请求方式："+request.method)
	print("请求path："+request.path)

	if request.method=="GET":
		name = request.GET['uname']
		age = request.GET.get('uage',None)
	else:
		name = request.POST['uname']
		age = request.POST.get('uage',None)
		print(request.POST.getlist("likes",None))
	return HttpResponse("name:%s, age:%s"%(name,age))

def verifycode(request):
    '''验证码实例'''
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('static/msyh.ttf', 23)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    #request.session['verifycode'] = rand_str
    #内存文件操作
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')