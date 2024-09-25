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
    user_type = serializers.ChoiceField(choices=Profile.USER_TYPE_CHOICES, required=False)
    years_of_experience = serializers.IntegerField(required=False, allow_null=True)
    specialties = serializers.CharField(required=False, allow_blank=True)
    portfolio_url = serializers.URLField(required=False, allow_blank=True)
    interests = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    content = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',
                  'user_type', 'years_of_experience', 'specialties', 'portfolio_url',
                  'interests', 'address', 'content', 'image')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if attrs.get('user_type') == 'professional':
            if attrs.get('years_of_experience') is None:
                raise serializers.ValidationError({"years_of_experience": "This field is required for professional users."})
            if not attrs.get('specialties'):
                raise serializers.ValidationError({"specialties": "This field is required for professional users."})

        return attrs

    def create(self, validated_data):
        try:
            password = validated_data.pop('password1')
            validated_data.pop('password2', None)

            # Extract profile data
            profile_data = {
                'user_type': validated_data.pop('user_type', 'amateur'),
                'years_of_experience': validated_data.pop('years_of_experience', None),
                'specialties': validated_data.pop('specialties', ''),
                'portfolio_url': validated_data.pop('portfolio_url', ''),
                'interests': validated_data.pop('interests', []),
                'address': validated_data.pop('address', ''),
                'content': validated_data.pop('content', ''),
                'image': validated_data.pop('image', None),
            }

            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=password,
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', '')
            )

            # Create or update profile
            Profile.objects.update_or_create(owner=user, defaults=profile_data)

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
