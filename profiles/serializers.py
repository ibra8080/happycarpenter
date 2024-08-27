from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)
    interests = serializers.ListField(
        child=serializers.CharField(), required=False)

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'created_at', 'updated_at', 'name',
                  'content', 'image', 'is_owner', 'user_type',
                  'years_of_experience', 'specialties', 'portfolio_url',
                  'interests', 'address']

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return 'https://res.cloudinary.com/ds5wgelgc/image/upload/v1722748736/default_post_ixahqa.jpg'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = self.get_image_url(instance)
        return ret

    def update(self, instance, validated_data):
        interests = validated_data.pop('interests', None)
        if interests is not None:
            instance.interests = interests

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
