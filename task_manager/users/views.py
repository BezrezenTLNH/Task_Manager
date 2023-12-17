from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from task_manager.mixins import CustomLoginRequiredMixin
from .mixins import CustomAccessMixin
from task_manager.tasks.models import TaskModel


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
        messages.success(self.request, _("Your profile has been successfully created!"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Please refill the form!"))
        return super().form_invalid(form)


class UserFormUpdateView(CustomLoginRequiredMixin,
                         CustomAccessMixin, UpdateView):

    model = User
    template_name = 'users/update.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        messages.success(self.request, _("User successfully changed"))
        return super().form_valid(form)


class UserFormDeleteView(CustomLoginRequiredMixin,
                         CustomAccessMixin, DeleteView):

    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        user = self.object
        task_autor = TaskModel.objects.filter(author_id=user.id)
        task_executor = TaskModel.objects.filter(executor_id=user.id)
        if task_autor or task_executor:
            messages.warning(
                self.request, _('Cannot delete user because it is in use')
            )
            return redirect('users')

        messages.success(self.request, _('User deleted successfully'))
        return super().form_valid(form)