# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import HelpRequest

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'fullname', 'phone', 'about', 'avatar', 'password1', 'password2']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 3}),
        }

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class HelpRequestForm(forms.ModelForm):
    class Meta:
        model = HelpRequest
        fields = ['title', 'category', 'description', 'name', 'email', 'phone', 'address', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }