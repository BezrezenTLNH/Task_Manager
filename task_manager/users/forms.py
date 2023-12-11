from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
        ]


class CustomUserUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
        ]
