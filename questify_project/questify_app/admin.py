from django.contrib import admin
from django.db.models import Count
from .models import (
    UserProfile, Kelas, Pencapaian,
    Transaksi, ModulPembelajaran, Soal, Nilai, JawabanUser, ContactMessage
)

# Registering each model in the Django admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')  # Menampilkan kolom user dan profile_picture di admin
    search_fields = ('user__username',)  # Menambahkan fitur pencarian berdasarkan username user
    list_filter = ('user',)  # Menambahkan filter berdasarkan user


@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('nama_kelas', 'harga', 'deskripsi_1', 'deskripsi_2')
    search_fields = ('nama_kelas',)
    list_filter = ('harga',)



class SoalInline(admin.TabularInline):
    model = Soal
    extra = 1  # Menambahkan satu form kosong untuk soal baru
    fields = ['pertanyaan', 'gambar', 'pilihan_a', 'pilihan_b', 'pilihan_c', 'pilihan_d', 'jawaban', 'nilai_jawaban']
    readonly_fields = ['nilai_jawaban']  # Nilai jawaban hanya bisa dilihat, tidak diubah manual


@admin.register(ModulPembelajaran)
class ModulPembelajaranAdmin(admin.ModelAdmin):
    list_display = ['judul', 'kelas', 'jumlah_soal', 'waktu_pengajaran', 'kategori', 'gratis']
    list_filter = ['kelas', 'kategori']
    search_fields = ['judul', 'deskripsi']
    inlines = [SoalInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        
        # Ambil instance modul
        modul = form.instance
        
        # Hitung jumlah soal
        total_soal = modul.soal.count()
        modul.jumlah_soal = total_soal
        modul.save(update_fields=['jumlah_soal'])

        # Perbarui nilai setiap soal jika ada soal
        if total_soal > 0:
            nilai_per_soal = 100 // total_soal  # Nilai per soal dibulatkan ke bawah
            for soal in modul.soal.all():
                soal.nilai_jawaban = nilai_per_soal
                soal.save(update_fields=['nilai_jawaban'])


@admin.register(Nilai)
class NilaiAdmin(admin.ModelAdmin):
    list_display = ('user', 'modul', 'jumlah_nilai', 'tanggal_percobaan', 'percobaan_ke')
    search_fields = ('user__email', 'modul__judul')
    list_filter = ('tanggal_percobaan',)


@admin.register(JawabanUser)
class JawabanUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'soal', 'modul', 'pilihan_user', 'status', 'waktu_jawab', 'percobaan_ke')
    search_fields = ('user__email', 'soal__pertanyaan', 'soal__modul__judul')
    list_filter = ('status', 'soal__modul')
    
    def modul(self, obj):
        return obj.soal.modul.judul
    modul.admin_order_field = 'soal__modul'  # Enable sorting
    modul.short_description = 'Modul Pembelajaran'


@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('user', 'kelas', 'status_pembayaran', 'tanggal_transaksi','batas_waktu_pembayaran','amount')
    search_fields = ('user__email', 'kelas__nama_kelas')
    list_filter = ['status_pembayaran']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'comment')
    search_fields = ('name', 'email')
    list_filter = ('name',)


@admin.register(Pencapaian)
class PencapaianAdmin(admin.ModelAdmin):
    list_display = ('nama', 'skor_minimum')