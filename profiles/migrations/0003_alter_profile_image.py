# Generated by Django 5.0.7 on 2024-08-14 17:46

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_address_profile_interests_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(default='default_profile_qdjgyp', max_length=255, verbose_name='image'),
        ),
    ]
