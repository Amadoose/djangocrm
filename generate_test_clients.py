import os
import django
from datetime import datetime, timedelta
import random
from faker import Faker
from django_countries import countries

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')
django.setup()

from website.models import Cliente  # Replace 'your_app' with your actual app name

fake = Faker()

# Gender choices from your model
GENDER_CHOICES = ['👨 Male', '👩 Female', '⚧️ Other']
GENDER_PROBABILITIES = [0.45, 0.45, 0.10]  # 45% male, 45% female, 10% other

# Loyalty levels from your model
LOYALTY_LEVELS = [
    ('bronze', '🥉 Bronze'),
    ('silver', '🥈 Silver'),
    ('gold', '🥇 Gold'),
    ('platinum', '💎 Platinum')
]
LOYALTY_PROBABILITIES = [0.50, 0.30, 0.15, 0.05]  # 50% bronze, 30% silver, etc.


def random_date(start_date, end_date):
    """Generate a random date between two dates"""
    time_between = end_date - start_date
    random_days = random.randrange(time_between.days)
    return start_date + timedelta(days=random_days)

def generate_clients(num_clients=1000):
    """Generate test clients for the database"""
    
    for i in range(num_clients):
        # Basic info
        gender = random.choices(GENDER_CHOICES, weights=GENDER_PROBABILITIES)[0]
        
        if gender == '👨 Male':
            first_name = fake.first_name_male()
        elif gender == '👩 Female':
            first_name = fake.first_name_female()
        else:
            first_name = fake.first_name()  # For 'Other' gender
            
        last_name = fake.last_name()
        maternal_last_name = fake.last_name() if random.random() < 0.8 else ""  # 80% have maternal last name
        
        # Email based on name
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
        
        # Phone number
        area_code = random.choice('+52')
        phone_number = f"{random.randint(1000000, 9999999)}"
        
        # Nationality - mostly Mexican with some foreigners
        nationality = 'MX' if random.random() < 0.85 else random.choice([c[0] for c in countries])
        
        # Dates
        birth_date = random_date(datetime(1950, 1, 1), datetime(2005, 12, 31))
        
        # Only some clients have anniversary dates (30% chance)
        if random.random() < 0.3:
            anniversary_date = random_date(birth_date, datetime(2023, 12, 31))
        else:
            anniversary_date = None
            
        # Loyalty level
        loyalty_level = random.choices(
            [level[0] for level in LOYALTY_LEVELS],
            weights=LOYALTY_PROBABILITIES
        )[0]
        
        # Create and save the client
        client = Cliente(
            nombre=first_name,
            apellido_paterno=last_name,
            apellido_materno=maternal_last_name,
            email=email,
            celular=phone_number,
            area_code=area_code,
            nacionalidad=nationality,
            fecha_nacimiento=birth_date,
            fecha_aniversario=anniversary_date,
            genero=gender,
            nivel_lealtad=loyalty_level
        )
        
        client.save()
        
        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1} clients...")

if __name__ == "__main__":
    print("Starting to generate test clients...")
    generate_clients()
    print("Finished generating 1000 test clients!")