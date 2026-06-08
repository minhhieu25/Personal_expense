from django.forms import ModelForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'email'}))
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


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'avatar']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),        
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password2 = cleaned_data.get('new_password2')

        # kiểm tra 2 mật khẩu có khớp không
        if new_password and new_password2 and new_password != new_password2:
            self.add_error("new_password2", "Mật khẩu mới không khớp!")
        
        # kiểm tra độ mạnh của mật khẩu
        if new_password:
            try:
                validate_password(new_password)
            except ValidationError as e:
                self.add_error("new_password", e)
                
        return cleaned_data