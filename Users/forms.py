from django.forms import ModelForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password'}))
    remember_me = forms.BooleanField(required=False) # False: khong bắt buộc


class RegisterFrom(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'username'})
        self.fields['email'].widget.attrs.update({'class': 'email'})
        self.fields['password1'].widget.attrs.update({'class': 'password1'})
        self.fields['password2'].widget.attrs.update({'class': 'password2'})
