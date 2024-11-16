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

# Create your views here.
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

    return render(request, 'questify_app/pages/index.html', {'form': form})

def register(request):
    form = CreateUserForm()


    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for {username}.  Please login')

            return redirect('login')

    context = {'form':form}
    return render(request, 'questify_app/pages/register.html', context)

def loginPage(request):

    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('questify_app:semuakelas')  
            else:
                messages.error(request, 'Username atau password salah')

    context = {}
    return render(request, 'questify_app/pages/login.html', context)

@login_required(login_url='/accounts/login/')
def semuakelas(request):
    return render(request, 'questify_app/pages/semuakelas.html')

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
def userprofile(request):
    return render(request, 'questify_app/pages/userprofile.html')

@login_required(login_url='/accounts/login/')
def detailkelas(request):
    return render(request, 'questify_app/pages/detailkelas.html')

@login_required(login_url='/accounts/login/')
def soal(request):
    return render(request, 'questify_app/pages/soal.html')

@login_required(login_url='/accounts/login/')
def pilihkelas(request):
    return render(request, 'questify_app/pages/pilihkelas.html')

@login_required(login_url='/accounts/login/')
def metodepembayaran(request):
    return render(request, 'questify_app/pages/metodepembayaran.html')

@login_required(login_url='/accounts/login/')
def cekbeli(request):
    return render(request, 'questify_app/pages/cekbeli.html')

@login_required(login_url='/accounts/login/')
def payment(request):
    return render(request, 'questify_app/pages/payment.html')

@login_required(login_url='/accounts/login/')
def daftartransaksi(request):
    return render(request, 'questify_app/pages/daftar_transaksi.html')

@login_required(login_url='/accounts/login/')
def detailtransaksi(request):
    return render(request, 'questify_app/pages/detailtransaksi.html')


