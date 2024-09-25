from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
import logging

logger = logging.getLogger(__name__)

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    # User fields
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    # Profile fields
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'profile')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        profile_data = attrs.get('profile', {})
        if profile_data.get('user_type') == 'professional':
            if profile_data.get('years_of_experience') is None:
                raise serializers.ValidationError({"years_of_experience": "This field is required for professional users."})
            if not profile_data.get('specialties'):
                raise serializers.ValidationError({"specialties": "This field is required for professional users."})

        return attrs

    def create(self, validated_data):
        try:
            profile_data = validated_data.pop('profile')
            password = validated_data.pop('password1')
            validated_data.pop('password2', None)

            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=password,
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', '')
            )

            Profile.objects.create(owner=user, **profile_data)

            return user
        except Exception as e:
            logger.exception(f"Error in create method: {str(e)}")
            raise serializers.ValidationError(f"Error creating user: {str(e)}")

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        user_data = super().to_representation(instance)
        profile_data = ProfileSerializer(instance.profile).data
        return {
            **user_data,
            'profile': profile_data,
        }
