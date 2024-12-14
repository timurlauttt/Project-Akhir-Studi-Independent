from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import ContactForm, CreateUserForm,ProfileUpdateForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUpdateForm
from .models import Pencapaian, UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Kelas
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import midtransclient

from django.http import JsonResponse
import midtransclient
from django.contrib.auth.models import User
import uuid

from django.http import JsonResponse
import midtransclient
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from .models import ModulPembelajaran, Soal, JawabanUser, Nilai, UserProfile, Kelas, PercobaanTerakhir, Transaksi
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now, timedelta
from django.utils.dateparse import parse_datetime
from django.db.models import Sum

from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import pytz
import logging



def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Simpan data dari form ke database
            form.save()

            # Mengirimkan email setelah formulir berhasil dikirim
            send_mail(
                'Pesan Kontak Baru',  # Subjek email
                f'Nama: {form.cleaned_data["name"]}\n'
                f'Telepon: {form.cleaned_data["phone"]}\n'
                f'Email: {form.cleaned_data["email"]}\n'
                f'Komentar: {form.cleaned_data["comment"]}',  # Isi email
                settings.EMAIL_HOST_USER,  # Pengirim
                [settings.EMAIL_HOST_USER],  # Penerima
                fail_silently=False,
            )

            # Menampilkan pesan sukses
            messages.success(request, "Pesan Anda telah berhasil dikirim!")
            return redirect('index')  # redirect untuk mengosongkan form
    else:
        form = ContactForm()

    # Ambil semua data kelas dari database
    kelas_list = Kelas.objects.all()

    return render(request, 'questify_app/pages/index.html', {
        'form': form,
        'kelas_list': kelas_list,  # Kirim data kelas ke template
    })

def register(request):
    form = CreateUserForm()


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for {username}.  Please login')

            return redirect('questify_app:login')

    context = {'form':form}
    return render(request, 'questify_app/pages/register.html', context)



def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect berdasarkan peran pengguna
            if user.is_staff or user.is_superuser:  # Admin atau staff
                return redirect(reverse('admin:index'))  # Halaman admin bawaan Django
            else:  # User biasa
                return redirect('questify_app:home')  # Halaman user biasa
        else:
            messages.error(request, 'Username atau password salah')

    return render(request, 'questify_app/pages/login.html')

@login_required
def home(request):

    # Ambil semua kelas
    semua_kelas = Kelas.objects.prefetch_related('modul_pembelajaran').all()

    # Ambil nilai user dengan jumlah_nilai > 70
    nilai_lebih_70 = Nilai.objects.filter(user=request.user, jumlah_nilai__gt=70)

    # Hitung total modul terselesaikan
    total_modul_terselesaikan = nilai_lebih_70.values('modul').distinct().count()

    # Hitung total modul yang tersedia
    total_modul = ModulPembelajaran.objects.count()

    # Hitung persentase penyelesaian modul
    persentase_penyelesaian = int(total_modul_terselesaikan / total_modul * 100) if total_modul > 0 else 0

    # Total skor user
    total_skor = nilai_lebih_70.aggregate(total=Sum('jumlah_nilai'))['total'] or 0

     # Ambil pencapaian tertinggi sesuai skor pengguna
    pencapaian = Pencapaian.objects.filter(skor_minimum__lte=total_skor).order_by('-skor_minimum').first()

    # Data penyelesaian per kelas
    data_kelas = []
    for kelas in semua_kelas:
        modul_ids = kelas.modul_pembelajaran.values_list('id', flat=True)
        modul_terselesaikan = Nilai.objects.filter(
            user=request.user,
            modul_id__in=modul_ids,
            jumlah_nilai__gt=70
        ).values('modul').distinct().count()
        total_modul = kelas.modul_pembelajaran.count()
        persentase = int(modul_terselesaikan / total_modul * 100) if total_modul > 0 else 0
        data_kelas.append({
            'nama_kelas': kelas.nama_kelas,
            'persentase': round(persentase, 2),
        })

    return render(request, 'questify_app/pages/home.html', {
        'total_modul': total_modul_terselesaikan,
        'persentase': round(persentase_penyelesaian, 2),
        'skor': total_skor,
        'data_kelas': data_kelas,
        'pencapaian': pencapaian,
    })



@login_required(login_url='/questify_app/login/')
def userprofile(request):
    user = request.user

    # Periksa apakah pengguna sudah memiliki profil
    if not hasattr(user, 'profile'):
        UserProfile.objects.create(user=user)  # Jika tidak ada, buatkan profil baru

    # Jika metode POST, proses perubahan profil
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda telah diperbarui!')
            return redirect('questify_app:userprofile')  # Redirect ke halaman profil setelah perubahan
    else:
        # Jika GET, tampilkan profil pengguna yang sedang login
        form = ProfileUpdateForm(instance=user)

    return render(request, 'questify_app/pages/userprofile.html', {'form': form, 'user': user})


@login_required(login_url='/questify_app/login/')
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('questify_app:userprofile')  # Ganti 'profile' dengan nama rute Anda
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'questify_app/pages/userprofile.html', {'form': form})




@login_required(login_url='/questify_app/login/')
def semuakelas(request):
    # Ambil semua kelas yang belum memiliki transaksi settlement
    kelas_list = Kelas.objects.exclude(transaksi__user=request.user, transaksi__status_pembayaran='settlement')
    return render(request, 'questify_app/pages/semuakelas.html', {'kelas_list': kelas_list})


@login_required(login_url='/questify_app/login/')
def payment(request):
    if request.method == 'POST':
        # Parse JSON data dari permintaan POST
        kelas_id = request.POST.get('kelas_id')
        amount = request.POST.get('amount')
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        
        print(user_id, amount)
        
        order_id = str(uuid.uuid4())

        snap = midtransclient.Snap(
            is_production=False,
            server_key='SB-Mid-server-IxGL8J0daVsu14JPWym77KPT'
        )
        
        # Build API parameter
        param = {
            "transaction_details": {
                "order_id": order_id,  # Sesuaikan order_id jika diperlukan
                "gross_amount": amount
            },
            "credit_card": {
                "secure": True
            },
            "customer_details": {
                "first_name": first_name,
                # "last_name": "pratama",
                # "email": "budi.pra@example.com",
                # "phone": "08111222333"
            }
        }

        # Buat transaksi di Midtrans dan dapatkan token
        transaction = snap.create_transaction(param)
        transaction_token = transaction['token']
        
        # Simpan data transaksi ke database
        kelas = Kelas.objects.get(id=kelas_id)
        user = User.objects.get(id=user_id)
        Transaksi.objects.create(
            user=user,
            kelas=kelas,
            amount=amount,
            link_payment="https://app.sandbox.midtrans.com/snap/v2/vtweb/" + transaction_token,
            order_id=order_id
        )
        
        # Mengembalikan token transaksi sebagai JSON
        return JsonResponse({"token": transaction_token})

    return JsonResponse({"error": "Invalid request"}, status=400)




@login_required(login_url='/questify_app/login/')
def pilihkelas(request, kelas_id):
    # Mendapatkan objek Kelas berdasarkan ID
    kelas = get_object_or_404(Kelas, id=kelas_id)
    
    # Memeriksa apakah pengguna telah menyelesaikan pembayaran untuk kelas ini
    is_subscribed = Transaksi.objects.filter(user=request.user, kelas=kelas, status_pembayaran='settlement').exists()
    
    # Mendapatkan semua modul tanpa filter
    modul_list = ModulPembelajaran.objects.filter(kelas=kelas)
    
    context = {
        'kelas': kelas,
        'modul_list': modul_list,
        'is_subscribed': is_subscribed,
    }
    
    return render(request, 'questify_app/pages/pilihkelas.html', context)




@login_required(login_url='/questify_app/login/')
def detailkelas(request, id):
    modul = get_object_or_404(ModulPembelajaran, id=id)
    kelas = modul.kelas  # Ambil kelas yang terkait dengan modul
    context = {
        'modul': modul,
        'kelas': kelas  # Kirimkan objek kelas ke template
    }
    return render(request, 'questify_app/pages/detailkelas.html', context)




@login_required(login_url='/questify_app/login/')
def hasilnilai(request):
    user = request.user
    hasil_data = (
        Nilai.objects.filter(user=user)
        .select_related('modul', 'modul__kelas')
        .order_by('-tanggal_percobaan', '-percobaan_ke', '-id')  # Urutkan berdasarkan tanggal, percobaan_ke, dan id
    )

    # Menambahkan informasi benar, salah, total soal untuk setiap nilai
    for result in hasil_data:
        # Filter JawabanUser berdasarkan percobaan_ke dan modul untuk menghitung benar dan salah
        total_benar = JawabanUser.objects.filter(user=user, percobaan_ke=result.percobaan_ke, soal__modul=result.modul, status=True).count()
        total_salah = JawabanUser.objects.filter(user=user, percobaan_ke=result.percobaan_ke, soal__modul=result.modul, status=False).count()

        # Menyimpan hasil ke dalam result untuk ditampilkan di template
        result.benar = total_benar
        result.salah = total_salah
        result.total_soal = result.modul.soal.count()  # Total soal dalam modul
        result.tanggal = result.tanggal_percobaan  # Tanggal percobaan

    return render(request, 'questify_app/pages/hasilnilai.html', {'hasil_data': hasil_data})


@login_required(login_url='/questify_app/login/')
def halamanselesai(request, modul_id, nilai_total):
    modul = get_object_or_404(ModulPembelajaran, id=modul_id)
    # Ambil percobaan terakhir yang dilakukan oleh pengguna untuk modul ini dari database
    percobaan_terakhir = PercobaanTerakhir.objects.filter(user=request.user, modul=modul).first()
    if percobaan_terakhir:
        percobaan_ke = percobaan_terakhir.percobaan_ke
    else:
        percobaan_ke = 1  # Jika tidak ada data percobaan sebelumnya, mulai dari percobaan pertama

    kelas = modul.kelas  # Ambil kelas yang terkait dengan modul


    jawaban_user = JawabanUser.objects.filter(
        user=request.user,
        soal__modul=modul,
        percobaan_ke=percobaan_ke
    )

    return render(request, 'questify_app/pages/halamanselesai.html', {
        'modul': modul,
        'nilai_total': nilai_total,
        'percobaan_ke': percobaan_ke,
        'jawaban_user': jawaban_user,
        'kelas': kelas,
    })



@login_required(login_url='/questify_app/login/')
def langganan(request):
    now_date = now()
    last_month_date = now_date - timedelta(days=30)
    transaksi_aktif = Transaksi.objects.filter(
        user=request.user,
        status_pembayaran='settlement',
        tanggal_transaksi__lte=now_date,
        tanggal_transaksi__gt=last_month_date
    )
    
    kelas_list = Kelas.objects.filter(transaksi__in=transaksi_aktif).distinct()
    
    for kelas in kelas_list:
        transaksi_terbaru = transaksi_aktif.filter(kelas=kelas).latest('tanggal_transaksi')
        kelas.transaksi_terbaru = transaksi_terbaru
    
    return render(request, 'questify_app/pages/langganan.html', {'kelas_list': kelas_list})



@login_required(login_url='/questify_app/login/')
def review(request, percobaan_ke, modul_id):
    user = request.user

    # Ambil data soal dan jawaban user berdasarkan percobaan dan modul
    jawaban_list = JawabanUser.objects.filter(
        user=user,
        soal__modul_id=modul_id,
        percobaan_ke=percobaan_ke
    )
    
    # Ambil objek modul berdasarkan ID modul
    modul = get_object_or_404(ModulPembelajaran, id=modul_id)

    # Hitung jumlah soal yang dijawab benar dan salah
    benar = jawaban_list.filter(status=True).count()
    salah = jawaban_list.filter(status=False).count()

    # Hitung durasi pengerjaan
    if jawaban_list.exists():
        waktu_mulai = jawaban_list.first().waktu_jawab
        waktu_selesai = jawaban_list.last().waktu_jawab
        durasi = waktu_selesai - waktu_mulai
    else:
        durasi = timezone.timedelta()

    # Format durasi menjadi HH:MM:SS tanpa desimal
    durasi_str = str(durasi).split('.')[0]

    # Hitung nilai akhir berdasarkan jumlah soal yang benar
    total_soal = jawaban_list.count()
    nilai = (benar / total_soal) * 100 if total_soal > 0 else 0  # Menghitung persentase benar

    # Ubah nilai menjadi integer untuk menghilangkan koma
    nilai = int(nilai)  # Mengkonversi nilai ke bilangan bulat tanpa koma

    # Ambil data nilai untuk percobaan ini (jika ada)
    nilai_data = Nilai.objects.filter(
        user=user,
        modul=modul,
        percobaan_ke=percobaan_ke
    ).first()

    # Jika data nilai belum ada, buat baru
    if not nilai_data:
        Nilai.objects.create(
            user=user,
            modul=modul,
            jumlah_nilai=nilai,
            waktu_pengajaran=durasi,
            percobaan_ke=percobaan_ke
        )

    context = {
        'jawaban_list': jawaban_list,
        'nilai': nilai,
        'total_soal': total_soal,
        'benar': benar,
        'salah': salah,
        'durasi': durasi_str,  # Menggunakan durasi yang sudah diformat
        'modul': modul,
        'percobaan_ke': percobaan_ke,
    }

    return render(request, 'questify_app/pages/review.html', context)


@login_required(login_url='/questify_app/login/')
def daftartransaksi(request):
    transaksi_list = Transaksi.objects.filter(user=request.user).order_by('-tanggal_transaksi')
    return render(request, 'questify_app/pages/daftar_transaksi.html', {'transaksi_list': transaksi_list})


@login_required(login_url='/questify_app/login/')
def detailtransaksi(request):
    return render(request, 'questify_app/pages/detailtransaksi.html')


@login_required(login_url='/questify_app/login/')
def soal(request, modul_id, soal_id=None):
    modul = get_object_or_404(ModulPembelajaran, id=modul_id)
    soal_list = Soal.objects.filter(modul=modul).order_by('id')

    # Cek percobaan terakhir di database untuk pengguna dan modul
    percobaan_terakhir = PercobaanTerakhir.objects.filter(user=request.user, modul=modul).first()
    if percobaan_terakhir:
        percobaan_ke = percobaan_terakhir.percobaan_ke
    else:
        percobaan_ke = 1  # Mulai dari percobaan pertama jika belum ada

    if soal_id is None:
        soal = soal_list.first()
        nomor_soal = 1
    else:
        soal = get_object_or_404(soal_list, id=soal_id)
        nomor_soal = list(soal_list).index(soal) + 1

    next_soal = soal_list.filter(id__gt=soal.id).first()
    is_last_question = next_soal is None

    pilihan_user = None
    if request.method == 'POST':
        pilihan_user = request.POST.get(f'pilihan_user_{soal.id}')
        if pilihan_user:
            status = pilihan_user == soal.jawaban
            JawabanUser.objects.create(
                user=request.user,
                soal=soal,
                pilihan_user=pilihan_user,
                status=status,
                percobaan_ke=percobaan_ke
            )

        if 'selesai' in request.POST:
            # Hitung nilai berdasarkan soal yang benar
            nilai_total = JawabanUser.objects.filter(
                user=request.user,
                soal__modul=modul,
                percobaan_ke=percobaan_ke,
                status=True
            ).aggregate(total_nilai=Sum('soal__nilai_jawaban'))['total_nilai'] or 0

            waktu_pengajaran = timedelta(seconds=request.session.get(f'modul_{modul_id}_time_spent', 0))
            # Cek apakah nilai sudah ada untuk percobaan ini
            nilai_data = Nilai.objects.filter(user=request.user, modul=modul, percobaan_ke=percobaan_ke).first()
            if not nilai_data:
                Nilai.objects.create(
                    user=request.user,
                    modul=modul,
                    jumlah_nilai=nilai_total,
                    waktu_pengajaran=waktu_pengajaran,
                    tanggal_percobaan=now(),
                    percobaan_ke=percobaan_ke
                )

            # Update percobaan ke untuk percakapan berikutnya
            percobaan_ke += 1
            PercobaanTerakhir.objects.update_or_create(
                user=request.user,
                modul=modul,
                defaults={'percobaan_ke': percobaan_ke}
            )

            return redirect('questify_app:halamanselesai', modul_id=modul.id, nilai_total=nilai_total)

        if next_soal:
            return redirect('questify_app:soal_detail', modul_id=modul.id, soal_id=next_soal.id)

    # Atur waktu pengerjaan
    session_key = f'modul_{modul_id}_time'
    start_time_str = request.session.get(f'{session_key}_start')
    end_time_str = request.session.get(f'{session_key}_end')

    if not start_time_str or not end_time_str:
        start_time = now()
        end_time = start_time + timedelta(minutes=modul.waktu_pengajaran)
        request.session[f'{session_key}_start'] = start_time.isoformat()
        request.session[f'{session_key}_end'] = end_time.isoformat()
    else:
        start_time = parse_datetime(start_time_str)
        end_time = parse_datetime(end_time_str)

    remaining_time = max(0, (end_time - now()).total_seconds())
    time_spent = max(0, (now() - start_time).total_seconds())
    request.session[f'modul_{modul_id}_time_spent'] = time_spent

    if remaining_time <= 0:
        # Waktu habis, kirim jawaban dengan nilai 0
        JawabanUser.objects.filter(user=request.user, percobaan_ke=percobaan_ke).delete()  # Hapus jawaban yang tidak terjawab
        return redirect('questify_app:pilihkelas', kelas_id=modul.kelas.id)  # Arahkan ke halaman pilih kelas


    pilihan = [
        ('A', soal.pilihan_a),
        ('B', soal.pilihan_b),
        ('C', soal.pilihan_c),
        ('D', soal.pilihan_d),
    ]

    return render(request, 'questify_app/pages/soal.html', {
        'soal': soal,
        'next_soal': next_soal,
        'nomor_soal': nomor_soal,
        'remaining_time': remaining_time,
        'is_last_question': is_last_question,
        'pilihan': pilihan,
        'pilihan_user': pilihan_user,
        'percobaan_ke': percobaan_ke,
        'modul': modul,
    })


# Konfigurasi logger untuk debugging
logger = logging.getLogger(__name__)

def midtrans_webhook(request):
    print('masukk atau ga? ')
    print(request)
    if request.method == 'POST':
        json_midtrans = json.loads(request.body)
        print(json_midtrans['transaction_status'])
        print('request', request)
        transaksi = Transaksi.objects.filter(order_id=json_midtrans['order_id']).last()
        print(transaksi)
        if transaksi : 
            transaksi.status_pembayaran=json_midtrans['transaction_status']
            print(transaksi.status_pembayaran)
            print(json_midtrans['transaction_status'])
            transaksi.save()
            print(transaksi.status_pembayaran)

    return JsonResponse({"error": "Invalid request method"}, status=200)