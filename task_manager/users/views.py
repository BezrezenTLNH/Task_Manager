from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from task_manager.mixins import CustomLoginRequiredMixin
from .mixins import CustomAccessMixin


# Create your views here.
class UsersView(ListView):

    template_name = 'users/users.html'
    model = User
    context_object_name = 'users'

class UserFormCreateView(CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your profile has been successfully created!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please refill the form!")
        return super().form_invalid(form)

class UserFormUpdateView(
    CustomLoginRequiredMixin,
    CustomAccessMixin,
    UpdateView):

    model = User
    template_name = 'users/update.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        messages.success(self.request, _('User successfully changed'))
        return super().form_valid(form)


class UserFormDeleteView(DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')


# class LoginUser(View):
#
#     def get(self, request, *args, **kwargs):
#         form = AuthenticationForm
#         return render(request, 'users/login.html', {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = AuthenticationForm(data=request.POST)
#
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, _('You are logged in'))
#             return redirect('index')
#
#         return render(request, 'users/login.html', {'form': form})
#
#     def logout_user(self):
#         logout(self)
#         messages.success(self, _('You are logged out'))
#         return redirect('/')