from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta

class Kelas(models.Model):  
    nama_kelas = models.CharField(max_length=100)
    harga = models.IntegerField()
    deskripsi_1 = models.TextField()
    deskripsi_2 = models.TextField(default="")  # Menambahkan nilai default

    def __str__(self):
        return self.nama_kelas

    def format_rupiah(self):
        """Format harga menjadi format Rupiah."""
        return f"Rp. {self.harga:,.0f}".replace(",", ".")


class ModulPembelajaran(models.Model):
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='modul_pembelajaran')
    judul = models.CharField(max_length=255)
    deskripsi = models.TextField()
    jumlah_soal = models.IntegerField(default=0)
    waktu_pengajaran = models.IntegerField()  # dalam menit
    kategori = models.CharField(max_length=100, default="General")  # Menambahkan field kategori
    gratis = models.BooleanField(default=True)

    def __str__(self):
        return self.judul

class Soal(models.Model):
    modul = models.ForeignKey(ModulPembelajaran, on_delete=models.CASCADE, related_name='soal')
    pertanyaan = models.TextField()
    pilihan_a = models.CharField(max_length=200)
    pilihan_b = models.CharField(max_length=200)
    pilihan_c = models.CharField(max_length=200)
    pilihan_d = models.CharField(max_length=200)
    jawaban = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    nilai_jawaban = models.IntegerField(default=10)
    gambar = models.ImageField(upload_to='soal_gambar/', blank=True, null=True)

    def __str__(self):
        return self.pertanyaan

    def save(self, *args, **kwargs):
        if self.modul:
            # Hitung jumlah soal saat ini di modul
            total_soal = self.modul.soal.exclude(id=self.id).count() + 1  # Termasuk soal baru
            if total_soal > 0:
                self.nilai_jawaban = 100 // total_soal
        super().save(*args, **kwargs)



class Nilai(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nilai_user')
    modul = models.ForeignKey(ModulPembelajaran, on_delete=models.CASCADE, related_name='nilai_user')
    jumlah_nilai = models.IntegerField()
    waktu_pengajaran = models.DurationField()
    tanggal_percobaan = models.DateTimeField(auto_now_add=True)
    percobaan_ke = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.modul.judul} - Percobaan {self.percobaan_ke} - Skor: {self.jumlah_nilai}"
    
    def get_durasi_formatted(self):
        return str(timedelta(seconds=self.waktu_pengajaran.total_seconds()))

    class Meta:
        ordering = ['user', 'modul', 'percobaan_ke']

class JawabanUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jawaban_user')
    soal = models.ForeignKey(Soal, on_delete=models.CASCADE, related_name='jawaban_user')
    pilihan_user = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    status = models.BooleanField(default=False)  # Benar atau salah
    waktu_jawab = models.DateTimeField(auto_now_add=True)
    percobaan_ke = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - Percobaan {self.percobaan_ke} - {self.soal.pertanyaan}"

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
    # total_pembayaran = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(default=0)
    link_payment = models.CharField(max_length=255,blank=True, null=True)

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

    def save(self, *args, **kwargs):
        # Jika ada gambar profil sebelumnya dan gambar baru diupload
        if self.pk and self.profile_picture:
            old_profile = UserProfile.objects.get(pk=self.pk)
            # Jika gambar berubah, hapus gambar yang lama
            if old_profile.profile_picture != self.profile_picture:
                if old_profile.profile_picture:
                    old_profile.profile_picture.delete(save=False)

        super().save(*args, **kwargs)


class PercobaanTerakhir(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    modul = models.ForeignKey(ModulPembelajaran, on_delete=models.CASCADE)
    percobaan_ke = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username} - {self.modul.judul} - Percobaan {self.percobaan_ke}"