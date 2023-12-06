from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy


# Create your views here.
class UsersView(ListView):

    template_name = 'users/users.html'
    model = User
    context_object_name = 'users'

class UserFormCreateView(CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm

class UserFormChangeView(UpdateView):
    template_name = 'users/update.html'
    form_class = CustomUserChangeForm

class UserFormDeleteView(DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
