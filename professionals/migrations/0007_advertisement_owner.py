# Generated by Django 5.0.7 on 2024-10-20 09:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0006_rename_reviewer_review_owner_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owned_advertisements', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
