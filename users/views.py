from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail
from django.conf import settings

from users.models import User
from users.forms import UserRegisterForm, UserForm, UserUpdateForm, UserPasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('books:books_list')
    template_name = 'users/register.html'
    extra_context = {
        'title' : 'User Registration'
    }

    def form_valid(self, form):

        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']
        user.set_password(password)
        user.save()

        send_mail('You are registered on Alcaeus Project!', 
                 (f'Hello, {username}.\n'
                  'You have been registered on Alcaues Project.\n'
                  'In case you need to recover your password you may use this email to do so.\n'
                  'Happy reading and research!'),
                  settings.EMAIL_HOST_USER, [email])

        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)

        return HttpResponseRedirect(self.success_url)


class UserLoginView(LoginView):
    template_name = 'users/login.html' 
    form_class = AuthenticationForm
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
        context['title'] = self.get_object().username + ' Profile'
        return context


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
        return context


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/update_profile.html'
    success_url = reverse_lazy('users:user_profile')
