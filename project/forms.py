from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Task

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(),
        strip=False,
    )


class CustomUserLogin(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            'password': forms.PasswordInput(),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'due']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control inp', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control inp', 'placeholder': 'Description'}),
            'complete': forms.CheckboxInput(),
            'due': forms.TextInput(attrs={'class': 'inp-date','id': 'datetime','type': 'datetime', 'placeholder': 'Due'}),
        }