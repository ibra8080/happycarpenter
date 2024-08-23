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
        if isinstance(obj.image, CloudinaryResource):
            return obj.image.url
        if isinstance(obj.image, str) and obj.image.startswith('http'):
            return obj.image
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
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = self.get_image(instance)
        return ret
