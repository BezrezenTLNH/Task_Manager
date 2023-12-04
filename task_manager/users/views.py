from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.models import User


# Create your views here.
class UsersView(ListView):

    template_name = 'users/users.html'
    model = User
    context_object_name = 'users'
