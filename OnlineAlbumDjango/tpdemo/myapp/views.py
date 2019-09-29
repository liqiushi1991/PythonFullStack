from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from myapp.models import District

# Create your views here.
def index(request):
	return render(request,"myapp/index.html") 

def demo1(request):
	'''模板的语法'''
	context={}
	context['name']="ZhangSan"
	context['a'] = [10,20,30]
	context['stu'] = {"name":"lisi","age":20}
	data=[
		{"name":"张翠山","sex":1,"age":40,'state':0},
		{"name":"殷素素","sex":0,"age":38,'state':2},
		{"name":"张无忌","sex":1,"age":20,'state':1},
		{"name":"赵敏","sex":0,"age":18,'state':2},
		]
	context['dlist']=data
	context['time'] = datetime.now
	context['m1']=100
	context['m2']=20
	return render(request,"myapp/demo1.html",context)

def demo2(request):
	'''模板继承'''
	return render(request,"myapp/demo2.html")

# 加载城市级联信息操作模板
def showdistrict(request):
    return render(request,"myapp/district.html")

# 加载对应的城市信息，并json格式ajax方式响应
def district(request,upid=0):
    dlist = District.objects.filter(upid=upid)
    list = []
    for ob in dlist:
        list.append({'id':ob.id,'name':ob.name})
    return JsonResponse({'data':list})