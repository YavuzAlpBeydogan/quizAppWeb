from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', include('quiz.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

]
