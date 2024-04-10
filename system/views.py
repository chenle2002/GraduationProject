from django.shortcuts import render, HttpResponse
from system import models


# Create your views here.

def login(request):
    user_name = request.GET.get('user_name')
    password = request.GET.get('password')
    if user_name is None:
        return HttpResponse("登陆失败，输入用户名为空")
    user = models.User.objects.filter(user_name=user_name)[0]
    if user is None:
        return HttpResponse("登陆失败，该用户不存在")
    if user.password == password:
        return HttpResponse("登陆成功")
    return HttpResponse("密码不正确")


def insert(request):
    user_name = request.GET.get('user_name')
    password = request.GET.get('password')
    if user_name is None:
        return HttpResponse("输入用户名为空")
    if password is None:
        return HttpResponse("输入密码为空")
    models.User.objects.create(user_name=user_name, password=password,status=1)

    return HttpResponse("新建用户成功")


def update(request):
    user_name = request.GET.get('user_name')
    password = request.GET.get('password')
    phone = request.GET.get('phone')
    obj = models.User.objects.get(user_name=user_name)  # 先查询
    obj.password = password
    obj.phone = phone
    obj.save()  # 将修改保存到数据库

    return HttpResponse("修改用户信息成功")


def delete(request):
    user_name = request.GET.get('user_name')
    if user_name is None:
        return HttpResponse("删除用户，输入用户名为空")
    models.User.objects.filter(user_name=user_name).delete()
    return HttpResponse("删除用户成功")


def logout(request):
    return HttpResponse('退出')
