from .views import logout,login
from django.urls import path

urlpatterns = [
    path('login/',login,name='login'),
    path('logout/', logout, name='logout'),
]
