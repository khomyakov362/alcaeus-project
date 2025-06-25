from django.urls import path
from users.apps import UsersConfig

from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user_login'),

]