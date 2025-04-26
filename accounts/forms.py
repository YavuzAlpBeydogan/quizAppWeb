from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Kullanıcı Adı",
        min_length=4,
        error_messages={
            'required': 'Kullanıcı adı zorunludur.',
            'min_length': 'Kullanıcı adı en az 4 karakter olmalıdır.'
        }
    )

    password1 = forms.CharField(
        label="Şifre",
        widget=forms.PasswordInput,
        help_text="Şifreniz en az 8 karakter, 1 büyük harf ve 1 sembol içermelidir.",
    )

    password2 = forms.CharField(
        label="Şifre (Tekrar)",
        widget=forms.PasswordInput,
        help_text="Şifreyi tekrar girin.",
    )

    class Meta:
        model = User
        fields = ('username',)

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Şifre en az 8 karakter olmalıdır.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Şifre en az 1 büyük harf içermelidir.")
        if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\-]', password):
            raise forms.ValidationError("Şifre en az 1 sembol içermelidir.")
        return password

from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Kullanıcı Adı',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı'})
    )
    password = forms.CharField(
        label='Şifre',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifre'})
    )
