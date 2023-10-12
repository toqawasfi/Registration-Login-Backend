from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from Reg_Log_App.views import registration_view,logout_view,send_email,password_reset
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Log in and obtain an authentication token
    path('login', obtain_auth_token, name='login'),
    
    # Register a new user
    path('register', views.registration_view, name='register'),
    
    # Log out and delete the user's authentication token
    path('logout', views.logout_view, name='logout'),
    
    # Send a password reset email
    path('send-email', views.send_email, name='send-email'),
    
    # Reset the user's password
    path('password_reset/<str:code>', views.password_reset, name='password_reset'),
]
  
 