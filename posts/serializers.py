from rest_framework import serializers
from .models import Post, Comment, Category
from django.contrib.humanize.templatetags.humanize import naturaltime


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = ['id', 'owner', 'post', 'created_at', 'updated_at', 'content']


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def validate_image(self, value):
        if value is None:
            return value
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if hasattr(value, 'image'):
            if value.image.height > 4096:
                raise serializers.ValidationError('Image height larger than 4096px!')
            if value.image.width > 4096:
                raise serializers.ValidationError('Image width larger than 4096px!')
        return value


    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    comments = CommentSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content', 'image', 
            'image_filter', 'comments', 'categories'
        ]
    
    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        post = Post.objects.create(**validated_data)
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(**category_data)
            post.categories.add(category)
        return post

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', [])
        instance = super().update(instance, validated_data)
        instance.categories.clear()
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(**category_data)
            instance.categories.add(category)
        return instance
