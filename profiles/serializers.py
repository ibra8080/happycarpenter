from rest_framework import serializers
from cloudinary.models import CloudinaryResource
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_image(self, obj):
        # Check if obj.image is a CloudinaryResource instance
        if isinstance(obj.image, CloudinaryResource):
            # Use the 'url' attribute to get the full URL of the image
            return obj.image.url

        # If obj.image is a string, assume it's already a full URL
        if isinstance(obj.image, str) and obj.image.startswith('http'):
            return obj.image

        # If it's not a CloudinaryResource or a URL string, handle accordingly
        return f'https://res.cloudinary.com/ds5wgelgc/image/upload/{obj.image}'

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'user_type',
            'years_of_experience', 'specialties', 'portfolio_url',
            'interests', 'address'
        ]
        read_only_fields = ['owner']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.content = validated_data.get('content', instance.content)
        
        # Handle image update
        new_image = validated_data.get('image')
        if new_image:
            # Here you would typically upload the new image to Cloudinary
            # and get the returned public_id or full URL
            # For now, we'll just use the filename as a placeholder
            instance.image = new_image.name
        
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Ensure the image field always returns a full URL
        ret['image'] = self.get_image(instance)
        return ret