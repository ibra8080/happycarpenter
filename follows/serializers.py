from rest_framework import serializers
from .models import Follow
from django.contrib.auth.models import User

class FollowSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    followed = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ['id', 'owner', 'followed', 'created_at']
        read_only_fields = ['owner']

    def validate_followed(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("You cannot follow yourself.")
        return value

    def create(self, validated_data):
        followed = validated_data.get('followed')
        owner = self.context['request'].user
        if Follow.objects.filter(owner=owner, followed=followed).exists():
            raise serializers.ValidationError("You are already following this user.")
        return Follow.objects.create(**validated_data)
