from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserForm, UserUpdateForm, UserPasswordChangeForm


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('')
    template_name = 'users/register.html'
    extra_context = {
        'title' : 'User Registration'
    }

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'users/login.html' 
    form_class = UserLoginForm
    extra_context = {
        'title' : 'Sign In'
    }


class UserProfileView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/profile.html'

    def get_object(self, queryset = None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().username + 'Profile'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update_profile.html'
    success_url = reverse_lazy('users:user_profile')

    def get_object(self, queryset = None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().username + 'Profile Update'


class UserLogoutView(LogoutView):
    pass


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users:user_profile')
