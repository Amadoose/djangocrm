from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record, Cliente
from django_countries.widgets import CountrySelectWidget



 #Customer model
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nacionalidad': CountrySelectWidget(attrs={'class': 'form-select'}),  # ✅ with flags
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_aniversario': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-select'}), #✅ Changed to Select widget
            'nivel_lealtad': forms.Select(attrs={'class': 'form-select'}),

        }
    
    def clean(self):
        cleaned_data = super().clean()
        celular = cleaned_data.get("celular", "")
        nacionalidad = cleaned_data.get("nacionalidad")

        from .utils import get_dial_code_by_country

        if nacionalidad and celular:
            dial_code = get_dial_code_by_country(nacionalidad)
            # Remove spaces, dashes, or duplicates
            number = celular.strip().replace(" ", "").replace("-", "")
            if not number.startswith(dial_code):
                cleaned_data["celular"] = f"{dial_code}{number}"
        return cleaned_data



class SignUpForm(UserCreationForm):
    ...
    email = forms.EmailField(
        label='',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Email Address'})
    )
    first_name = forms.CharField(
        label='',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label='',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Last Name'})
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
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': ''}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': ''}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': ''}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': ''}),
        }



