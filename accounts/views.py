from django.shortcuts import render, redirect
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

from .forms import CustomLoginForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()

    return render(request, 'quiz/login.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.shortcuts import render, redirect
from quiz.models import QuizResult, UserAnswer

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user:
            # İlgili kullanıcıya ait tüm verileri sil
            QuizResult.objects.filter(user=user).delete()
            UserAnswer.objects.filter(user=user).delete()
            # Kullanıcıyı sil
            user.delete()
            logout(request)
            messages.success(request, "Hesabınız ve tüm verileriniz silindi.")
            return redirect('home')  # Anasayfa URL ismini yaz
        else:
            messages.error(request, "Şifre yanlış. Lütfen tekrar deneyin.")
    return render(request, 'accounts/delete_account.html')
