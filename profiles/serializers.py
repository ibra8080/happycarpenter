from rest_framework import serializers
from .models import Profile
from professionals.serializers import ReviewSerializer

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'user_type',
            'years_of_experience', 'specialties', 'portfolio_url',
            'interests', 'address', 'public_view', 'reviews'
        ]

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

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['years_of_experience', 'specialties', 'portfolio_url', 'interests', 'address', 'content', 'image']

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        user_type = instance.user_type if instance else attrs.get('user_type')

        if user_type == 'professional':
            if attrs.get('years_of_experience') is None:
                raise serializers.ValidationError({"years_of_experience": "This field is required for professional users."})
            if not attrs.get('specialties'):
                raise serializers.ValidationError({"specialties": "This field is required for professional users."})

        return attrs
