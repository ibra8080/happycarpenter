from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from profiles.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    # Essential User fields
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    # Essential Profile field
    user_type = serializers.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES, required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'user_type')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        validated_data.pop('password2')
        
        user = User.objects.create_user(**validated_data)
        
        Profile.objects.create(owner=user, user_type=user_type)
        
        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def to_representation(self, instance):
        if isinstance(instance, dict):
            user_data = super().to_representation(instance['user'])
            return {
                **user_data,
                'refresh': instance['refresh'],
                'access': instance['access'],
            }
        return super().to_representation(instance)
