# Generated by Django 5.2.1 on 2025-06-13 18:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_activity_airline_hotel_operator_transport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='alias',
        ),
        migrations.AlterField(
            model_name='hotel',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='price_per_night',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, '★☆☆☆☆ (Poor)'), (2, '★★☆☆☆ (Fair)'), (3, '★★★☆☆ (Good)'), (4, '★★★★☆ (Very Good)'), (5, '★★★★★ (Excellent)')], null=True, verbose_name='Star Rating'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='contact_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='transport',
            name='contact_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
