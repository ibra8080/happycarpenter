from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('amateur', 'Amateur'),
        ('professional', 'Professional'),
    ]

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = CloudinaryField('image', default='default_profile_azwy8y')

    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='amateur')
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    specialties = models.CharField(max_length=255, blank=True)
    portfolio_url = models.URLField(max_length=200, blank=True)
    interests = ArrayField(
        models.CharField(max_length=100), blank=True, default=list)
    address = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            owner=instance,
            name=instance.get_full_name() or instance.username
        )
    else:
        instance.profile.name = instance.get_full_name() or instance.username
        instance.profile.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance, name=instance.username)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
