from django.db import models
from django_countries.fields import CountryField

# Create your models here.

class Record(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the model was created")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)    

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")
    
class Cliente(models.Model):
    # Gender choices
    GENDER_CHOICES = [
        ('masculino', 'Male'),
        ('femenino', 'Female'),
        ('otro', 'Other'),
        ('prefiero_no_decir', 'Rather not say'),
    ]

    # CharField for short strings (names, etc.)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    email = models.EmailField(unique=True)  # EmailField with uniqueness constraint
    celular = models.CharField(max_length=15)
    nacionalidad = CountryField(blank_label='(Select country)', default='MX')

    # Date fields for birthdays and anniversaries
    fecha_nacimiento = models.DateField()
    fecha_aniversario = models.DateField(blank=True, null=True)

    # Gender w choices and loyalty level as plain text
    genero = models.CharField(max_length=20, choices=GENDER_CHOICES, default='prefiero_no_decir')
    nivel_lealtad = models.CharField(max_length=20,
                                     choices=[('bronze', '🥉 Bronze'), ('silver', '🥈 Silver'), ('gold', '🥇 Gold'),('platinum','💎 Platinum',)], default='bronze', blank=True, null=True)

    def __str__(self):
        # This is how each instance will be represented as a string
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno or ''}".strip()