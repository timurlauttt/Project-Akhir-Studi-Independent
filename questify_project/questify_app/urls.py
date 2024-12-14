from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


app_name = "questify_app"

urlpatterns = [
    path('', views.index, name='index'),  # Halaman index sebagai landing-page
    path('semuakelas/', views.semuakelas, name='semuakelas'),
    path('hasilnilai/', views.hasilnilai, name='hasilnilai'),
    path('halamanselesai/<int:modul_id>/halamanselesai/<int:nilai_total>/', views.halamanselesai, name='halamanselesai'),
    path('langganan/', views.langganan, name='langganan'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('review/<int:percobaan_ke>/<int:modul_id>/', views.review, name='review'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('detailkelas/<int:id>/', views.detailkelas, name='detailkelas'),
    path('pilihkelas/<int:kelas_id>/', views.pilihkelas, name='pilihkelas'),
    path('payment/', views.payment, name='payment'),
    path('daftar_transaksi/', views.daftartransaksi, name='daftartransaksi'),
    path('detailtransaksi/', views.detailtransaksi, name='detailtransaksi'),
    path('soal/<int:modul_id>/soal/', views.soal, name='soal'),
    path('soal/<int:modul_id>/soal/<int:soal_id>/', views.soal, name='soal_detail'),
    path('home/', views.home, name='home'),

    path('midtrans_webhook', csrf_exempt(views.midtrans_webhook), name='midtrans_webhook'),
]