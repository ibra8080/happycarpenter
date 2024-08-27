from django.db import models
from django.contrib.auth.models import User


class Advertisement(models.Model):
    professional = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='advertisements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    professional = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name='reviews_received')
    reviewer = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name='reviews_given')
    content = models.TextField()
    rating = models.IntegerField(choices=[
        (i, i) for i in range(1, 6)])  # 1-5 star rating
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.professional.username} by {self.reviewer.username}"


class JobOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    ]
    professional = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='job_offers')
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='job_offers_made')
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
            max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Job offer for {self.professional.username} from {self.client.username}"
