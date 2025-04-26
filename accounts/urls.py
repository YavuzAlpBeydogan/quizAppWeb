from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),

    # Tek ve doğru login yolu:
    path('login/', LoginView.as_view(
        template_name='accounts/login.html',  # ya da senin login.html yolun
        authentication_form=CustomLoginForm
    ), name='login'),
]
