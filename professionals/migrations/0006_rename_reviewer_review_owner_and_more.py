# Generated by Django 5.0.7 on 2024-10-13 20:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0005_review_updated_at_alter_review_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='reviewer',
            new_name='owner',
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('professional', 'owner')},
        ),
    ]
