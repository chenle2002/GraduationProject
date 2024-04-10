from .views import predict_text
from django.urls import path

urlpatterns = [
    path('predict/', predict_text, name='predict'),
]
