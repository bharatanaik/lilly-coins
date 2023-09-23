from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import LillyUser

class LillyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = LillyUser
        fields = ('username', 'email', 'password1', 'password2')

class LillyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = LillyUser
        fields = ('username', 'amount')