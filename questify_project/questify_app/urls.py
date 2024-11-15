from django.urls import path
from . import views

app_name = "questify_app"

urlpatterns = [
    path('', views.index, name='index'),  # Halaman index sebagai landing-page
    path('semuakelas/', views.semuakelas, name='semuakelas'),
    path('hasilnilai/', views.hasilnilai, name='hasilnilai'),
    path('halamanselesai/', views.halamanselesai, name='halamanselesai'),
    path('langganan/', views.langganan, name='langganan'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('review/', views.review, name='review'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('metodepembayaran/', views.metodepembayaran, name='metodepembayaran'),
    path('cekbeli/', views.cekbeli, name='cekbeli'),
    path('payment/', views.payment, name='payment'),
    path('daftar_transaksi/', views.daftartransaksi, name='daftartransaksi'),
    path('detailtransaksi/', views.detailtransaksi, name='detailtransaksi'),

]
