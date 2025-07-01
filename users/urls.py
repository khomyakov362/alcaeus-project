from django.conf import settings
from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('update/', views.UserUpdateView.as_view(), name='user_update'),
    path('change-password/', 
         views.UserPasswordChangeView.as_view(), 
         name='user_change_password'),
    path('reset-password/', 
         views.UserPasswordResetView.as_view(), 
         name='user_reset_password'),
    path('reset-password/done/', 
         views.UserPasswordResetDoneView.as_view(), 
         name='user_reset_password_done'),
    path('reset-password-confirm/<uidb64>/<token>/', 
         views.UserPasswordResetConfirmView.as_view(), 
         name='user_reset_password_confirm'),
    path('reset-password-complete/', 
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ), 
         name='user_reset_password_complete'),
]