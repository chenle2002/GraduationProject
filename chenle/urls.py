from . import views
from .views import predict_text, delete, process_excel, judge_exist, download, getinfobyid
from django.urls import path

urlpatterns = [
    path('predict/', predict_text, name='predict'),
    path('delete/', delete, name='delete'),
    path('process_excel/', process_excel, name='process_excel'),
    path('judge_exist/', judge_exist, name='judge_exist'),
    path('download/', download, name='download'),
    path('getinfobyid/', getinfobyid, name='getinfobyid'),
]
