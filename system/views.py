from django.shortcuts import render,HttpResponse
# Create your views here.

def login(request):
    return HttpResponse('登录成功')


def logout(request):
    return HttpResponse('退出')

def index(request):
    return HttpResponse('主页面')






