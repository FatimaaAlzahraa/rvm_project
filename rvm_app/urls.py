from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('deposits/', views.create_deposit, name='create_deposit'),
    path('user/summary/', views.user_summary, name='user_summary'),
]