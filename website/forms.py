from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record

class SignUpForm(UserCreationForm):
    ...
    email = forms.EmailField(
        label='',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Correo electrónico'})
    )
    first_name = forms.CharField(
        label='',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'first name'})
    )
    last_name = forms.CharField(
        label='',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'last name'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Confirm Password'}),
        }

#Add record form class
class AddRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        exclude = (User,)
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {            
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Nombre Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Apellido Apellido'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '111 222 3333'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'juanrodriguez@email.com'}),
        }

