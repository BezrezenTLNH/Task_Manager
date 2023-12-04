from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from task_manager.users import views


urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
]
