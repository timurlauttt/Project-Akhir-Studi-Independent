from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Route ke halaman index 
    path('semuakelas/', views.semuakelas, name='semuakelas'),  # Route untuk halaman semuakelas  
]
