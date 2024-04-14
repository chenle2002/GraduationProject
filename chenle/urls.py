from . import views
from .views import predict_text,delete
from django.urls import path

urlpatterns = [
    path('predict/', predict_text, name='predict'),
    path('delete/', delete, name='delete'),
]
