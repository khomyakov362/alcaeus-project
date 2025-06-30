from django.conf import settings
from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LogoutView

from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
]