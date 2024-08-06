from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Advertisement, Review, JobOffer


class AdvertisementSerializer(serializers.ModelSerializer):
    professional = serializers.ReadOnlyField(source='professional.username')

    class Meta:
        model = Advertisement
        fields = ['id', 'professional', 'title', 'description', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    professional = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(profile__user_type='professional'))
    reviewer = serializers.ReadOnlyField(source='reviewer.username')

    class Meta:
        model = Review
        fields = ['id', 'professional', 'reviewer', 'content', 'rating', 'created_at']

class JobOfferSerializer(serializers.ModelSerializer):
    professional = serializers.ReadOnlyField(source='professional.username')
    client = serializers.ReadOnlyField(source='client.username')

    class Meta:
        model = JobOffer
        fields = ['id', 'professional', 'client', 'title', 'description', 'budget', 'created_at', 'status']