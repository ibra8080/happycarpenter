from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Advertisement, Review, JobOffer

class AdvertisementSerializer(serializers.ModelSerializer):
    professional = serializers.SerializerMethodField()
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

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
            'updated_at'
        ]

    def get_professional(self, obj):
        return {
            'id': obj.professional.id,
            'username': obj.professional.username
        }

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
            'created_at'
        ]

    def create(self, validated_data):
        return Review.objects.create(**validated_data)


class JobOfferSerializer(serializers.ModelSerializer):
    professional = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(profile__user_type='professional'))
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
        read_only_fields = ['client', 'created_at', 'status']

    def validate_professional(self, value):
        if not value.profile.user_type == 'professional':
            raise serializers.ValidationError("The selected user is not a professional.")
        return value


    def create(self, validated_data):
        client = self.context['request'].user
        return JobOffer.objects.create(client=client, **validated_data)
