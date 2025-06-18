from django.db import models
from django.forms import ValidationError
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator


# Create your models here.    
class Cliente(models.Model):
    
    GENDER_CHOICES = [
        ('👨 Male', '👨 Male'),
        ('👩 Female', '👩 Female'),
        ('⚧️ Other', '⚧️ Other')       
    ]

    # CharField for short strings (names, etc.)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100) 
    email = models.EmailField(unique=True)  
    celular = models.CharField(max_length=15, help_text="Phone number wihout area code")
    area_code = models.CharField(max_length=10, default="+52", help_text="Area code with country code")
    nacionalidad = CountryField(blank_label='(Select country)', default='MX')

    # Date fields for birthdays and anniversaries
    fecha_nacimiento = models.DateField()
    fecha_aniversario = models.DateField(blank=True, null=True)

    # Gender w choices and loyalty level as plain text
    genero = models.CharField(max_length=20, choices=GENDER_CHOICES, default='👩 Female')
    nivel_lealtad = models.CharField(max_length=20,
                                     choices=[('bronze', '🥉 Bronze'), ('silver', '🥈 Silver'), ('gold', '🥇 Gold'),('platinum','💎 Platinum',)], default='bronze', blank=True, null=True)

    def __str__(self):
        # This is how each instance will be represented as a string
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno or ''}".strip()   
    

class Hotel(models.Model):

    AMENITY_CHOICES = [
        ('minibar', 'Minibar'),
        ('pool', 'Alberca'),
        ('gym', 'Gym'),
        ('spa', 'Spa'),
        ('restaurant', 'Restaurante'),
        ('bar', 'Bar'),
        ('beach', 'Playa'),
        ('breakfast', 'Desayuno incluido'),
        ('pets', 'Mascotas'),
    ]    
        
    STAR_RATING_CHOICES = [
        (1, '★☆☆☆☆ (Poor)'),
        (2, '★★☆☆☆ (Fair)'),
        (3, '★★★☆☆ (Good)'),
        (4, '★★★★☆ (Very Good)'),
        (5, '★★★★★ (Excellent)'),       
    ]

    name = models.CharField(max_length=200)    
    location = models.CharField(max_length=200)    
    contact_email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)  # Allow blank if optional
    rating = models.PositiveSmallIntegerField(choices=STAR_RATING_CHOICES, null=True, blank=True, verbose_name="Star Rating")
    website = models.URLField()
    # Add validation to price
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)]  # Prevent negative prices
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='hotels_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='hotels_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active status",
        help_text="Designates whether this hotel should be treated as active."
    )

    amenities = models.CharField(
        max_length=200,  # Increased to accommodate multiple selections
        blank=True,
        help_text="Select multiple amenities"
    )  

    def __str__(self):
        return self.name

class Airline(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(
        max_length=3,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[A-Z]{2,3}$',
                message='IATA code must be 2-3 uppercase letters (e.g., "AA" or "BAW")',
                code='invalid_iata_code'
            )
        ],
        verbose_name="IATA Code"
    )    
    country = models.CharField(max_length=100)    
    phone = models.CharField(max_length=20)
    website = models.URLField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='airlines_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='airlines_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active status",
        help_text="Designates whether this hotel should be treated as active."
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

class Activity(models.Model):

    ACTIVITY_TYPE_CHOICES = [
        ('safari', 'Safari'),
        ('tour', 'Tour'),
        ('excursion', 'Excursiones'),
        ('cultural', 'Actividad Cultural'),
        ('deportiva', 'Deportiva'),
        ('aventura', 'Aventura'),
    ]


    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=ACTIVITY_TYPE_CHOICES, verbose_name="Tipo de actividad")
    location = models.CharField(max_length=200)
    duration = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)    
    supplier = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name

class Operator(models.Model):

    SERVICE_TYPE = [
        ('aerolinea', 'Aerolinea'),
        ('hotel', 'Hotel'),
        ('actividades', 'Actividades'),
        ('terrestre', 'Transporte terrestre'),
        ('maritimo', 'Transporte Maritimo'),        
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=SERVICE_TYPE, verbose_name="Tipo de servicio")
    location = models.CharField(max_length=200)    
    contact_email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    website = models.URLField()    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='operators_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='operators_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active status",
        help_text="Designates whether this hotel should be treated as active."
    )
    

    def __str__(self):
        return self.name

class Transport(models.Model):
    TRANSPORT_TYPES = [
        ('bus', 'Bus'),
        ('taxi', 'Taxi'),
        ('rental_car', 'Rental Car'),
        ('train', 'Train'),
        ('shuttle', 'Shuttle'),
        ('boat', 'Boat'),
    ]
    
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=TRANSPORT_TYPES)
    location = models.CharField(max_length=200)
    contact_email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    website = models.URLField()
    capacity = models.IntegerField(null=True, blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transports_created')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transports_modified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active status",
        help_text="Designates whether this hotel should be treated as active."
    )

    def __str__(self):
        return f"{self.name} - {self.get_type_display()}"
    

class Folio(models.Model):
    TIPO_VIAJE_CHOICES = [
        ('honeymoon', '💕 Luna de Miel'),
        ('anniversary', '🎉 Aniversario'),
        ('birthday', '🎂 Cumpleaños'),
        ('vacation', '🏖️ Vacaciones'),
        ('business', '💼 Viaje de Negocios'),
        ('family', '👨‍👩‍👧‍👦 Viaje Familiar'),
        ('graduation', '🎓 Graduación'),
        ('wedding', '💒 Boda'),
        ('other', '✨ Otro'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='folios')
    agente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='folios_asignados')
    tipo_viaje = models.CharField(max_length=50, choices=TIPO_VIAJE_CHOICES, default='vacation', verbose_name="Celebración")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Folio'
        verbose_name_plural = 'Folios'

    def __str__(self):
        return f"Folio #{self.id} - {self.cliente.nombre} {self.cliente.apellido_paterno}"