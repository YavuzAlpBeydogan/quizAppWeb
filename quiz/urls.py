from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<int:language_id>/', views.quiz_view, name='quiz'),
    path('result/', views.result_view, name='result'), 
    path('history/', views.history_view, name='history'),
]
