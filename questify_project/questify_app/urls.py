from django.urls import path
from . import views


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
    # path('soal/', views.soal, name='soal'),
    path('pilihkelas/<int:kelas_id>/', views.pilihkelas, name='pilihkelas'),
    path('metodepembayaran/', views.metodepembayaran, name='metodepembayaran'),
    path('cekbeli/', views.cekbeli, name='cekbeli'),
    path('payment/', views.payment, name='payment'),
    path('daftar_transaksi/', views.daftartransaksi, name='daftartransaksi'),
    path('detailtransaksi/', views.detailtransaksi, name='detailtransaksi'),
    path('soal/<int:modul_id>/soal/', views.soal, name='soal'),
    path('soal/<int:modul_id>/soal/<int:soal_id>/', views.soal, name='soal_detail'),
    path('home/', views.home, name='home'),
]
