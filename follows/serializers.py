from rest_framework import serializers
from .models import Follow

class FollowSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follow
        fields = ['id', 'owner', 'followed', 'followed_name', 'created_at']