from .views import testapi
from django.urls import path

urlpatterns = [
    path('testapi/', testapi, name='testapi'),
]
