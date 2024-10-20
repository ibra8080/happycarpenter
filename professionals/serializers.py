from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Advertisement, Review, JobOffer
import logging

logger = logging.getLogger(__name__)


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

    def validate(self, data):
        logger.info(f"Validating data: {data}")
        if self.instance:  # This is an update
            title = data.get('title', self.instance.title)
            description = data.get('description', self.instance.description)
        else:  # This is a create
            title = data.get('title')
            description = data.get('description')

        if not title:
            logger.error("Title is required")
            raise serializers.ValidationError("Title is required")
        if not description:
            logger.error("Description is required")
            raise serializers.ValidationError("Description is required")
        return data

    def update(self, instance, validated_data):
        logger.info(f"Updating instance: {instance}")
        logger.info(f"Validated data: {validated_data}")
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.place = validated_data.get('place', instance.place)
        if 'image' in validated_data:
            instance.image = validated_data['image']
        instance.save()
        logger.info(f"Instance updated: {instance}")
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    professional = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(profile__user_type='professional'),
        required=False
    )
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Review
        fields = ['id', 'professional', 'owner', 'content', 'rating', 'created_at', 'updated_at']

    def validate_professional(self, value):
        if not value.profile.user_type == 'professional':
            raise serializers.ValidationError("The selected user is not a professional.")
        return value

class JobOfferSerializer(serializers.ModelSerializer):
    professional = serializers.SerializerMethodField()
    client = serializers.ReadOnlyField(source='client.username')
    advertisement = AdvertisementSerializer(read_only=True)
    advertisement_id = serializers.PrimaryKeyRelatedField(
        queryset=Advertisement.objects.all(), 
        source='advertisement', 
        write_only=True
    )

    class Meta:
        model = JobOffer
        fields = [
            'id',
            'professional',
            'client',
            'advertisement',
            'advertisement_id',
            'title',
            'description',
            'budget',
            'created_at',
            'status',
            'feedback',
            'status_updated_at'
        ]
        read_only_fields = ['client', 'created_at', 'status', 'feedback', 'status_updated_at']

    def get_professional(self, obj):
        return {
            'id': obj.professional.id,
            'username': obj.professional.username
        }

    def validate_professional(self, value):
        if not value['id'].profile.user_type == 'professional':
            raise serializers.ValidationError("The selected user is not a professional.")
        return value['id']
