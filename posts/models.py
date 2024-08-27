from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    image_filter_choices = [
        ('furniture', 'Furniture'),
        ('antiques', 'Antiques'),
        ('renovation&repair', 'Renovation & repair'),
        ('artworks', 'Artworks'),
        ('tools', 'Tools'),
        ('construction', 'Construction'),
        ('other', 'Other')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = CloudinaryField(
        'image',
        folder='happy_carpenter',
        blank=True,
        null=True,
        transformation={
            'width': 1000,
            'height': 1000,
            'crop': 'limit'
        },
        resource_type='auto'
    )
    image_filter = models.CharField(
        max_length=32, choices=image_filter_choices, default='normal'
    )
    categories = models.ManyToManyField(
        Category, related_name='posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
            Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
