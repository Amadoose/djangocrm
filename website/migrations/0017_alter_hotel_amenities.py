# Generated by Django 5.2.1 on 2025-06-16 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_auto_20250615_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='amenities',
            field=models.CharField(blank=True, help_text='Select multiple amenities', max_length=200),
        ),
    ]
