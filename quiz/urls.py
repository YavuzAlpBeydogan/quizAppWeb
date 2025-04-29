from django.urls import path
from . import views
from .views import signup_view
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<int:language_id>/', views.quiz_view, name='quiz'),
    path('result/', views.result_view, name='result'), 
    path('history/', views.history_view, name='history'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('accounts/', include('accounts.urls')),

]
