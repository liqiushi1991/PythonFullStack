from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from datetime import datetime

from common.models import Users,Types,Goods

# 公共信息加载函数

def loadinfo(request):
    lists = Types.objects.filter(pid=0)
    context = {'typelist':lists}
    context['tid'] = 0
    return context

def index(request):
    '''项目前台首页'''
    context = loadinfo(request)

    return render(request,"web/index.html",context)

def lists(request,pIndex=1):
    '''商品列表页'''
    context = loadinfo(request)
    #查询商品信息
    mod = Goods.objects
    mywhere = []

    #判断封装搜索条件
    tid = int(request.GET.get("tid",0))
    if tid > 0:
        list = mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid))
        mywhere.append('tid='+str(tid))
    else:
        list = mod.filter()

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list,8) #以8条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表

    #封装模板中需要的信息
    context['goodslist'] = list2
    context['plist'] = plist
    context['pIndex'] = pIndex
    context['pIndex'] = pIndex
    context['mywhere'] = mywhere
    context['tid'] = tid

    return render(request,"web/list.html",context)


def listfiltered(request, tid=0):
    '''商品列表页'''
    context = loadinfo(request)
    #查询商品信息
    mod = Goods.objects
    mywhere = []

    tid = int(tid)
    #判断封装搜索条件
    if tid == 0:
        list = mod.filter(typeid__in=Types.objects.only('id').filter()).order_by('clicknum')[:5]
        # mywhere.append('tid='+str(tid))
    else:
        list = mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid)).order_by('addtime')[:4]

    print(tid)
    print(list)
    context['goodslist'] = list
    context['tid'] = tid

    return render(request,"web/listf.html", context)

def detail(request,gid):
    '''商品详情页'''
    context = loadinfo(request)
    ob = Goods.objects.get(id=gid)
    ob.clicknum += 1
    ob.save()
    context['goods'] = ob
    return render(request,"web/detail.html",context)

# ==============前台会员登录====================
def login(request):
    '''会员登录表单'''
    return render(request,'web/login.html')

def dologin(request):
    '''会员执行登录'''
    # 校验验证码
    verifycode = request.session['verifycode']
    code = request.POST['code']
    if verifycode != code:
        context = {'info':'验证码错误！'}
        return render(request,"web/login.html",context)

    try:
        #根据账号获取登录者信息
        user = Users.objects.get(username=request.POST['username'])
        #判断当前用户是否是后台管理员用户
        if user.state == 0 or user.state == 1:
            # 验证密码
            import hashlib
            m = hashlib.md5() 
            m.update(bytes(request.POST['password'],encoding="utf8"))
            if user.password == m.hexdigest():
                # 此处登录成功，将当前登录信息放入到session中，并跳转页面
                request.session['vipuser'] = user.toDict()
                return redirect(reverse('index'))
            else:
                context = {'info':'登录密码错误！'}
        else:
            context = {'info':'此用户为非法用户！'}
    except:
        context = {'info':'登录账号错误！'}
    return render(request,"web/login.html",context)

def logout(request):
    '''会员退出'''
    # 清除登录的session信息
    del request.session['vipuser']
    # 跳转登录页面（url地址改变）
    return redirect(reverse('login'))

def register(request):
    '''会员注册表单'''
    return render(request, 'web/register.html')


def doregister(request):
    try:
        ob = Users()
        ob.username = request.POST['username']
        if request.POST['password'] == request.POST['repassword']:
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'], encoding="utf8"))
            ob.password = m.hexdigest()
            ob.state = 1
            ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.save()
            context = {"info": "添加成功！请重新登录"}
            return render(request, 'web/login.html', context)
        else:
            context = {'info': '两次输入密码不一致！'}
            return render(request, 'web/register.html', context)

    except Exception as err:
        print(err)
        context = {'info': '注册账号错误！'}
    return render(request, 'web/register.html', context)
