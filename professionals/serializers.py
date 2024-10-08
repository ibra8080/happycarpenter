from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Advertisement, Review, JobOffer

class AdvertisementSerializer(serializers.ModelSerializer):
    professional = serializers.ReadOnlyField(source='professional.username')

    class Meta:
        model = Advertisement
        fields = [
            'id', 
            'professional', 
            'title', 
            'description', 
            'image', 
            'place', 
            'created_at',
            'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    professional = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(profile__user_type='professional'))
    reviewer = serializers.ReadOnlyField(source='reviewer.username')

    class Meta:
        model = Review
        fields = [
            'id',
            'professional',
            'reviewer',
            'content',
            'rating',
            'created_at']

    def create(self, validated_data):
        return Review.objects.create(**validated_data)


class JobOfferSerializer(serializers.ModelSerializer):
    professional = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    client = serializers.ReadOnlyField(source='client.username')
    advertisement = serializers.PrimaryKeyRelatedField(queryset=Advertisement.objects.all())

    class Meta:
        model = JobOffer
        fields = [
            'id',
            'professional',
            'client',
            'advertisement',
            'title',
            'description',
            'budget',
            'created_at',
            'status'
        ]
