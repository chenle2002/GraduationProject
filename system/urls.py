from .views import logout, login, predict, insert, update, delete
from django.urls import path

urlpatterns = [
    path('login/', login, name='login'),
    path('insert/', insert, name='insert'),
    path('update/', update, name='update'),
    path('delete/', delete, name='delete'),
    path('logout/', logout, name='logout'),

    path('predict/', predict, name='predict'),
]
