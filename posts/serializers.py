from rest_framework import serializers
from .models import Post, Comment, Category
from django.contrib.humanize.templatetags.humanize import naturaltime
from cloudinary.utils import cloudinary_url
import logging


logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        return obj.created_at.isoformat()

    def get_updated_at(self, obj):
        return obj.updated_at.isoformat()

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'post', 'created_at', 'updated_at', 'content'
        ]

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    image = serializers.ImageField(required=False)
    likes_count = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return cloudinary_url(obj.image.public_id)[0]
        return None

    def validate_image(self, value):
        if value is None:
            return value
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if hasattr(value, 'image'):
            if value.image.height > 4096:
                raise serializers.ValidationError(
                        'Image height larger than 4096px!')
            if value.image.width > 4096:
                raise serializers.ValidationError(
                        'Image width larger than 4096px!')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_likes_count(self, obj):  
        return obj.likes.count()

    comments = CommentSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content', 'image',
            'image_filter', 'comments', 'categories', 'likes_count'
        ]

    def create(self, validated_data):
        logger.info(f"Creating post with data: {validated_data}")
        categories_data = validated_data.pop('categories', [])
        image = validated_data.pop('image', None)
        post = Post.objects.create(**validated_data)
        if image:
            post.image = image
            post.save()
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(**category_data)
            post.categories.add(category)
        logger.info(f"Post created successfully: {post}")
        return post

    def update(self, instance, validated_data):
        logger.info(f"Updating post {instance.id} with data: {validated_data}")
        categories_data = validated_data.pop('categories', [])
        image = validated_data.pop('image', None)
        instance = super().update(instance, validated_data)
        if image:
            instance.image = image
            instance.save()
        instance.categories.clear()
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(**category_data)
            instance.categories.add(category)
        logger.info(f"Post {instance.id} updated successfully")
        return instance
