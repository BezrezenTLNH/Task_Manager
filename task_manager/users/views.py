from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render(request, 'users/index.html')

class IndexUsersView(ListView):

    template_name = 'users/users.html'
    model = User
    context_object_name = 'users'

# @require_http_methods(['GET', 'POST'])
# def get(request):
