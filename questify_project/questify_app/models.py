from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Kelas(models.Model):
    nama_kelas = models.CharField(max_length=100)
    harga = models.IntegerField()
    deskripsi = models.TextField()

    def __str__(self):
        return self.nama_kelas

class ModulPembelajaran(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='modul_pembelajaran')
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    jumlah_soal = models.IntegerField()
    waktu_pengajaran = models.IntegerField()  # dalam menit

    def __str__(self):
        return self.judul

class Soal(models.Model):
    modul = models.ForeignKey(ModulPembelajaran, on_delete=models.CASCADE, related_name='soal')
    pertanyaan = models.TextField()
    pilihan_a = models.CharField(max_length=255)
    pilihan_b = models.CharField(max_length=255)
    pilihan_c = models.CharField(max_length=255)
    pilihan_d = models.CharField(max_length=255)
    jawaban = models.CharField(max_length=1)  # 'A', 'B', 'C', 'D'
    nilai_jawaban = models.IntegerField()

class Nilai(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nilai')
    modul = models.ForeignKey(ModulPembelajaran, on_delete=models.CASCADE, related_name='nilai')
    jumlah_nilai = models.IntegerField()
    waktu_pengajaran = models.DateTimeField(auto_now_add=True)
    tanggal_percobaan = models.DateTimeField(auto_now_add=True)

class JawabanUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jawaban_user')
    soal = models.ForeignKey(Soal, on_delete=models.CASCADE, related_name='jawaban_user')
    pilihan_user = models.CharField(max_length=1)  # 'A', 'B', 'C', 'D'
    status = models.BooleanField(default=False)  # benar atau salah
    waktu_jawab = models.DateTimeField(auto_now_add=True)

class MetodePembayaran(models.Model):
    nama_metode = models.CharField(max_length=50)
    no_rek = models.CharField(max_length=20)

    def __str__(self):
        return self.nama_metode

class Transaksi(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('gagal', 'Gagal'),
        ('berhasil', 'Berhasil'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaksi')
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='transaksi')
    metode_pembayaran = models.ForeignKey(MetodePembayaran, on_delete=models.CASCADE, related_name='transaksi', null=True)
    status_pembayaran = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    tanggal_transaksi = models.DateTimeField(auto_now_add=True)
    batas_waktu_pembayaran = models.DateTimeField(default=datetime.now)
    total_pembayaran = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaksi oleh {self.user.username} untuk {self.kelas.nama_kelas}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    comment = models.TextField()

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username