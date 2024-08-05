# forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm as AuthPasswordChangeForm
from .models import User  # Use only the custom User model
from django import forms

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User  # Ensure the custom User model is used
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(UserChangeForm):
    password = None  # Remove password field from user update form

    class Meta:
        model = User  # Ensure the custom User model is used
        fields = ['username', 'first_name', 'last_name', 'email']

class PasswordChangeForm(AuthPasswordChangeForm):
    class Meta:
        model = User  # Ensure the custom User model is used
