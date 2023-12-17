from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.statuses.models import StatusModel
from .filters import TaskFilter
from .forms import TaskModelForm
from .mixins import CustomAccessMixin
from .models import TaskModel


class SpecificTaskView(generic.DetailView):
    model = TaskModel
    template_name = 'tasks/view_task.html'
    context_object_name = 'task'


class TasksView(CustomLoginRequiredMixin, generic.ListView):
    template_name = 'tasks/tasks.html'
    model = TaskModel
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = TaskModel.objects.all()
        tasks_filtered = TaskFilter(
            self.request.GET, queryset=tasks, request=self.request
        )
        return tasks_filtered

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = StatusModel.objects.all()
        context['executors'] = User.objects.all()
        context['filter'] = self.get_queryset()
        return context


class CreateTaskView(CustomLoginRequiredMixin, generic.CreateView):
    template_name = 'tasks/create.html'
    form_class = TaskModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request, _('Task has been successfully created')
        )
        return super().form_valid(form)


class UpdateTaskView(CustomLoginRequiredMixin, generic.UpdateView):
    model = TaskModel
    template_name = 'tasks/update.html'
    form_class = TaskModelForm

    def form_valid(self, form):
        messages.success(self.request, _('Task successfully changed'))
        return super().form_valid(form)


class DeleteTaskView(CustomAccessMixin, generic.DeleteView):
    model = TaskModel
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        messages.success(self.request, _('Task deleted successfully!'))
        return super().form_valid(form)
