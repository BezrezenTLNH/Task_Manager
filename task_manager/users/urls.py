from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from task_manager import views


urlpatterns = [
    path('/', views.index),
]

# urlpatterns += i18n_patterns(
#     path("i18n/", include("django.conf.urls.i18n")),
#     path('', views.index),
#     prefix_default_language=False
# )
