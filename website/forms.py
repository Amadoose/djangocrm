from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record, Cliente
from django_countries.widgets import CountrySelectWidget

class ClienteForm(forms.ModelForm): 
    class Meta:
        model = Cliente
        fields = [
            'nombre', 'apellido_paterno', 'apellido_materno', 'email',
            'nacionalidad', 'celular', 'fecha_nacimiento', 'fecha_aniversario',
            'genero', 'nivel_lealtad', 'area_code'
        ]        

        labels = {
            'nombre': 'First Name',
            'apellido_paterno': 'Last Name',
            'apellido_materno': 'Second Last Name',
            'email': 'Email Address',
            'nacionalidad': 'Nationality',
            'celular': 'Phone Number',
            'fecha_nacimiento': 'Date of Birth',
            'fecha_aniversario': 'Anniversary Date',
            'genero': 'Gender',
            'nivel_lealtad': 'Loyalty Level'
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nacionalidad': CountrySelectWidget(attrs={'class': 'form-select'}),            
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_aniversario': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'nivel_lealtad': forms.Select(attrs={'class': 'form-select'}),

            'celular': forms.TextInput(attrs={
                'class': 'form-control phone-number-input',
                'placeholder': '123-456-7890',
                'maxlength' : '12',
                'id': 'phoneNumber',
            }),

            # Area code field - separate and editable
            'area_code': forms.TextInput(attrs={
                'class': 'form-control area-code-input',
                'placeholder': '+52',
                'maxlength': '10',
                'value': '+52',
                'id': 'areaCode'
            }),
        }

    # Add a method to get the full phone number
    def get_full_phone(self):
        area_code = self.cleaned_data.get('area_code', '+52')
        celular = self.cleaned_data.get('celular', '')
        return f"+{area_code}{celular}" if celular else area_code
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        celular = self.cleaned_data.get('celular', '')
        if celular:
            # Ensure we don't duplicate the area code
            if celular.startswith(self.cleaned_data.get('area_code', '+52')):
                # Already formatted correctly
                instance.celular = celular
        
        if commit:
            instance.save()
        return instance    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.celular:
            # Split existing phone number
            if '-' in self.instance.celular:
                area_code, number = self.instance.celular.split('-', 1)
                self.initial['area_code'] = area_code
                self.initial['celular'] = number

    def clean(self):
        cleaned_data = super().clean()
        celular = cleaned_data.get('celular', '').strip()
        
        if celular:
            # Remove ALL non-digits (no formatting in DB)
            cleaned_data['celular'] = ''.join(c for c in celular if c.isdigit())
        
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
