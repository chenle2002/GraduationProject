from django.shortcuts import render, HttpResponse
from system import models


# Create your views here.
def testapi(request):
    return HttpResponse("接口访问成功")