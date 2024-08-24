from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)
    interests = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'created_at', 'updated_at', 'name',
                  'content', 'image', 'is_owner', 'user_type',
                  'years_of_experience', 'specialties', 'portfolio_url',
                  'interests', 'address']

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.image:
            ret['image'] = instance.image.url
        else:
            ret['image'] = 'https://res.cloudinary.com/ds5wgelgc/image/upload/v1722748736/default_post_ixahqa.jpg'
        return ret

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'interests':
                setattr(instance, attr, value or [])
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
