from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    username = forms.CharField(
        label="Логин",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "form_field"})
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form_field"}))
    password1 = forms.CharField(
        label="Пароль",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form_field"}),
    )
    class Meta:
        model = User
        fields = ('username', 'email', "password1")