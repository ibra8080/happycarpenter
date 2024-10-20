from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Advertisement, Review, JobOffer
import logging

logger = logging.getLogger(__name__)


class AdvertisementSerializer(serializers.ModelSerializer):
    professional = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Advertisement
        fields = [
            'id', 
            'professional', 
            'owner',
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
            raise serializers.ValidationError({"title": "Title is required"})
        if not description:
            logger.error("Description is required")
            raise serializers.ValidationError({"description": "Description is required"})
        return data
    
    def validate_image(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:  # 2MB limit
                raise serializers.ValidationError("Image file too large (max 2MB)")
            if not value.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise serializers.ValidationError("Unsupported image format. Use PNG, JPG, JPEG or GIF.")
        return value

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class JobOfferSerializer(serializers.ModelSerializer):
    professional = UserSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    advertisement_details = serializers.SerializerMethodField()

    class Meta:
        model = JobOffer
        fields = [
            'id', 'professional', 'client', 'advertisement', 'title',
            'description', 'budget', 'created_at', 'status', 'feedback',
            'status_updated_at', 'advertisement_details'
        ]
        read_only_fields = ['created_at', 'status', 'feedback', 'status_updated_at']

    def get_advertisement_details(self, obj):
        if obj.advertisement:
            return {
                'id': obj.advertisement.id,
                'title': obj.advertisement.title,
                'image': obj.advertisement.image.url if obj.advertisement.image else None,
                'place': obj.advertisement.place,
                'owner': UserSerializer(obj.advertisement.owner).data
            }
        return None
        