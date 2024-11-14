from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Route ke halaman index 
    path('semuakelas/', views.semuakelas, name='semuakelas'),  # Route untuk halaman semuakelas  
    path('hasilnilai/', views.hasilnilai, name='hasilnilai'),  # Route untuk halaman hasilnilai  
    path('halamanselesai/', views.halamanselesai, name='halamanselesai'),  # Route untuk halaman selesai
    path('langganan/', views.langganan, name='langganan'),  # Route untuk halaman langganan
    path('login/', views.loginPage, name='login'), 
    path('register/', views.register, name='register'),
    path('review/', views.review, name='review'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('metodepembayaran/', views.metodepembayaran, name='metodepembayaran'),
    path('cekbeli/', views.cekbeli, name='cekbeli'),
    path('payment/', views.payment, name='payment'),

]
