# forms.py
from django import forms
from .models import ContactMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control w-100', 
                'id': 'name', 
                'placeholder': 'Masukkan nama', 
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control w-100', 
                'id': 'phone', 
                'placeholder': 'Masukkan nomor telepon', 
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control w-100', 
                'id': 'email', 
                'placeholder': 'Masukkan email', 
                'required': True
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control w-100', 
                'id': 'comment', 
                'placeholder': 'Tulis komentar Anda', 
                'rows': 4, 
                'required': True
            }),
        }

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Nama depan')
    last_name = forms.CharField(max_length=30, required=True, help_text='Nama belakang')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)  # Menangani gambar profil (opsional)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']  # Sesuaikan dengan field yang Anda inginkan

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inisialisasi profile_picture dari UserProfile jika sudah ada profil
        if hasattr(self.instance, 'profile') and self.instance.profile:
            self.fields['profile_picture'].initial = self.instance.profile.profile_picture

    def save(self, commit=True):
        # Simpan data user
        user = super().save(commit)
        # Simpan data profile_picture ke UserProfile jika ada
        if 'profile_picture' in self.cleaned_data:
            user.profile.profile_picture = self.cleaned_data['profile_picture']
            user.profile.save()
        return user