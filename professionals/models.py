from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Advertisement(models.Model):
    professional = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='advertisements')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_advertisements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)
    place = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.owner_id:
            self.owner = self.professional
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    professional = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_received')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_given')
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['professional', 'owner']

    def __str__(self):
        return f"Review for {self.professional.username} by {self.owner.username}"


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
    advertisement = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, related_name='job_offers', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
            max_length=20, choices=STATUS_CHOICES, default='pending')
    feedback = models.TextField(blank=True, null=True)
    status_updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Job offer for {self.professional.username} from {self.client.username}"

    def update_status(self, new_status, feedback=None):
        self.status = new_status
        self.feedback = feedback
        self.status_updated_at = timezone.now()
        self.save()
