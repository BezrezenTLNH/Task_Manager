from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


class LoginUserFormView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    next_page = reverse_lazy("index")
    form_class = AuthenticationForm
    success_message = _("You are logged in")

    def form_invalid(self, form):
        messages.error(
            self.request,
            _(
                "Please enter the correct username and password. "
                "Both fields can be case sensitive."
            ),
        )
        return self.render_to_response(self.get_context_data(form=form))


class LogoutUserView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)