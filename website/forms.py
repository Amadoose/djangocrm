from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    """
    Custom user creation form that extends Django's built-in UserCreationForm.
    This form is used for user registration.
    """

    email = forms.EmailField(label='', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    first_name = forms.CharField(label= '', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'first name'}))
    last_name = forms.CharField(label= '', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last name'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
            'email': 'Enter a valid email address.',
            'password1': 'Your password must contain at least 8 characters.',
            'password2': 'Enter the same password as before, for verification.',
        }