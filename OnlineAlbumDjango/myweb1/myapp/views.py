from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Stu
# Create your views here.
def index(request):
    return HttpResponse('Hello')

def stu(request):
    mod = Stu.objects
    list = mod.all()
    stu = mod.get(id='2')
    print(stu)

    return HttpResponse('Ok')