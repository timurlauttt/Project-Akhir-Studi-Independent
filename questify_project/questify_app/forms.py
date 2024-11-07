# forms.py
from django import forms
from .models import ContactMessage

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