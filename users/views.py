from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)
from django.core.mail import send_mail
from django.conf import settings

from users.models import User
from django.contrib.auth.forms import AuthenticationForm
from users.forms import (
    UserRegisterForm, 
    UserForm, 
    UserUpdateForm, 
    UserPasswordChangeForm
)


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


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:user_reset_password_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:user_reset_password_complete')


class RemoveAccountView(DeleteView):
    model = User
    template_name = 'users/remove_account.html'
    extra_context = {
        'title': 'Deleting User Account'
    }
    success_url = reverse_lazy('books:books_list')

    def get_object(self, queryset=None):
        object_ = super().get_object()

        if object_ != self.request.user:
            raise Http404
        
        return object_

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        logout(request)
        self.object.delete()

        return HttpResponseRedirect(success_url)

