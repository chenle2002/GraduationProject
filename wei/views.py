from django.http import JsonResponse, HttpResponse

from wei.SearchQueries import controller
import os
import time

import pandas as pd
from django.views.decorators.csrf import csrf_exempt

from chenle.TextPredictor import predictor_instance
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework import status
from django.http import JsonResponse, HttpResponse

from GraduationProject import settings
from chenle import entity
from chenle.serializers.Patent import PatentSerializer
from rest_framework.pagination import PageNumberPagination

def get_ipc_from_text(request):
    text = request.GET.get('text')
    if (text!=None and len(text)>0):
        res = controller.get_ipc_from_text(text)
        return JsonResponse({'status': status.HTTP_200_OK, 'data': res},
                            status=status.HTTP_200_OK)
    else:
        return HttpResponse('输入文本为空')

def get_topic_syntax(request):
    text = request.GET.get('text')
    if (text != None and len(text) > 0):
        res = controller.get_topic_syntax(text)
        return JsonResponse({'status': status.HTTP_200_OK, 'data': res},
                            status=status.HTTP_200_OK)
    else:
        return HttpResponse('输入文本为空')

@csrf_exempt
def load_target_data(request):
    excel_file = request.FILES['file']
    if(excel_file!=None):
        res = controller.load_target_data(excel_file)
        if(res):
            return HttpResponse('上传成功')
        else:
            return HttpResponse('上传失败')
    else:
        return HttpResponse('未上传文件')

@csrf_exempt
def load_other_data(request):
    excel_file = request.FILES['file']
    if (excel_file != None):
        res = controller.load_other_data(excel_file)
        if (res):
            return HttpResponse('上传成功')
        else:
            return HttpResponse('上传失败')
    else:
        return HttpResponse('未上传文件')

def build_syntax_by_target(request):
    res = controller.build_syntax_by_target()
    if (res != None):
        return JsonResponse({'status': status.HTTP_200_OK, 'data': res},
                            status=status.HTTP_200_OK)
    else:
        return HttpResponse('未上传文件')