from django.contrib import admin
from .models import (
    UserProfile,Kelas, MetodePembayaran,
    Transaksi, ModulPembelajaran, Soal, Nilai, JawabanUser, ContactMessage
)

# Registering each model in the Django admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')  # Menampilkan user dan gambar profil di daftar admin
    search_fields = ('user__username',)  # Membolehkan pencarian berdasarkan username
    list_filter = ('user',)  # Filter berdasarkan pengguna
    
    # Menambahkan kemampuan untuk mengedit profil melalui admin
    def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(UserProfile, UserProfileAdmin)


@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('nama_kelas', 'harga', 'deskripsi')
    search_fields = ('nama_kelas',)
    list_filter = ('harga',)


@admin.register(ModulPembelajaran)
class ModulPembelajaranAdmin(admin.ModelAdmin):
    list_display = ('kelas', 'judul', 'jumlah_soal', 'waktu_pengajaran')
    search_fields = ('judul',)
    list_filter = ('kelas',)

@admin.register(Soal)
class SoalAdmin(admin.ModelAdmin):
    list_display = ('modul', 'pertanyaan', 'jawaban', 'nilai_jawaban')
    search_fields = ('pertanyaan',)
    list_filter = ('modul',)

@admin.register(Nilai)
class NilaiAdmin(admin.ModelAdmin):
    list_display = ('user', 'modul', 'jumlah_nilai', 'tanggal_percobaan')
    search_fields = ('user__email', 'modul__judul')
    list_filter = ('tanggal_percobaan',)

@admin.register(JawabanUser)
class JawabanUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'soal', 'pilihan_user', 'status', 'waktu_jawab')
    search_fields = ('user__email', 'soal__pertanyaan')
    list_filter = ('status',)

@admin.register(MetodePembayaran)
class MetodePembayaranAdmin(admin.ModelAdmin):
    list_display = ('nama_metode', 'no_rek')
    search_fields = ('nama_metode', 'no_rek')

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('user', 'kelas', 'metode_pembayaran', 'status_pembayaran', 'tanggal_transaksi','batas_waktu_pembayaran','total_pembayaran')
    search_fields = ('user__email', 'kelas__nama_kelas', 'metode_pembayaran__nama_metode')
    list_filter = ('status_pembayaran', 'metode_pembayaran')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'comment')
    search_fields = ('name', 'email')
    list_filter = ('name',)