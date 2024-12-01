from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUpdateForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Kelas
from .models import ModulPembelajaran,Transaksi
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import midtransclient

from django.http import JsonResponse
import midtransclient
from .models import Kelas, Transaksi
from django.contrib.auth.models import User
import uuid

#Create your views here.

def index(request):
    data = "Hello, Questify!"  # Variabel data untuk ditampilkan
    return render(request, 'questify_app/index.html', context={'data': data})


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
    return render(request, 'questify_app/pages/home.html')

@login_required(login_url='/accounts/login/')
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


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('questify_app:userprofile')  # Ganti 'profile' dengan nama rute Anda
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'questify_app/pages/userprofile.html', {'form': form})


@login_required(login_url='/accounts/login/')
def semuakelas(request):
    kelas_list = Kelas.objects.all()
    return render(request, 'questify_app/pages/semuakelas.html', {'kelas_list': kelas_list})
from django.http import JsonResponse
import midtransclient
from .models import Kelas, Transaksi
from django.contrib.auth.models import User

def payment(request):
    if request.method == 'POST':
        # Parse JSON data dari permintaan POST
        kelas_id = request.POST.get('kelas_id')
        amount = request.POST.get('amount')
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        
        print(user_id, amount)
        
        snap = midtransclient.Snap(
            is_production=False,
            server_key='SB-Mid-server-IxGL8J0daVsu14JPWym77KPT'
        )
        
        # Build API parameter
        param = {
            "transaction_details": {
                "order_id": str(uuid.uuid4()),  # Sesuaikan order_id jika diperlukan
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
            link_payment="https://app.sandbox.midtrans.com/snap/v2/vtweb/" + transaction_token
        )
        
        # Mengembalikan token transaksi sebagai JSON
        return JsonResponse({"token": transaction_token})

    return JsonResponse({"error": "Invalid request"}, status=400)


def pilihkelas(request):
    modul_list = ModulPembelajaran.objects.select_related('kelas').all()
    print("Jumlah modul:", modul_list.count())  # Menampilkan jumlah modul di terminal
    context = {
        'modul_list': modul_list
    }
    return render(request, 'questify_app/pages/pilihkelas.html', context)


def detailkelas(request, id):
    modul = get_object_or_404(ModulPembelajaran, id=id)
    context = {
        'modul': modul
    }
    return render(request, 'questify_app/pages/detailkelas.html', context)


@login_required(login_url='/accounts/login/')
def hasilnilai(request):
    return render(request, 'questify_app/pages/hasilnilai.html')

@login_required(login_url='/accounts/login/')
def halamanselesai(request):
    return render(request, 'questify_app/pages/halamanselesai.html')

@login_required(login_url='/accounts/login/')
def langganan(request):
    return render(request, 'questify_app/pages/langganan.html')

@login_required(login_url='/accounts/login/')
def review(request):
    return render(request, 'questify_app/pages/review.html')

@login_required(login_url='/accounts/login/')
def soal(request):
    return render(request, 'questify_app/pages/soal.html')

@login_required(login_url='/accounts/login/')
def metodepembayaran(request):
    return render(request, 'questify_app/pages/metodepembayaran.html')

@login_required(login_url='/accounts/login/')
def cekbeli(request):
    return render(request, 'questify_app/pages/cekbeli.html')

# @login_required(login_url='/accounts/login/')
# def payment(request):
#     return render(request, 'questify_app/pages/payment.html')

@login_required(login_url='/accounts/login/')
def daftartransaksi(request):
    return render(request, 'questify_app/pages/daftar_transaksi.html')

@login_required(login_url='/accounts/login/')
def detailtransaksi(request):
    return render(request, 'questify_app/pages/detailtransaksi.html')

#keperluang midtrans
# @login_required
# def initiate_payment(request):
#     # Ambil metode pembayaran dari parameter URL
#     bank = request.GET.get('bank')
    
#     if not bank:
#         return HttpResponse("Metode pembayaran tidak ditemukan", status=400)
    
#     # Logika untuk memulai proses pembayaran menggunakan Midtrans
#     # Misalnya, mengatur parameter dan mengirim permintaan ke Midtrans
    
#     # Redirect atau tampilkan halaman sesuai kebutuhan setelah proses pembayaran
#     return HttpResponse(f"Proses pembayaran menggunakan bank {bank} dimulai.", status=200)