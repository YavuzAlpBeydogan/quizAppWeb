from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', include('quiz.urls')),  # home view burada zaten tanımlı
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
