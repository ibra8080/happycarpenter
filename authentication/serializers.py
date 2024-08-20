from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from profiles.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from profiles.serializers import ProfileSerializer



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    # Profile fields
    user_type = serializers.ChoiceField(choices=Profile.USER_TYPE_CHOICES, required=True, write_only=True)
    years_of_experience = serializers.IntegerField(required=False, write_only=True)
    specialties = serializers.CharField(required=False, write_only=True)
    portfolio_url = serializers.URLField(required=False, write_only=True)
    interests = serializers.ListField(child=serializers.CharField(max_length=100), required=False, write_only=True)
    address = serializers.CharField(max_length=255, required=False, write_only=True)
    profile_image = serializers.ImageField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name',
                  'user_type', 'years_of_experience', 'specialties', 'portfolio_url',
                  'interests', 'address', 'profile_image')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if attrs['user_type'] == 'professional':
            if not attrs.get('years_of_experience'):
                raise serializers.ValidationError({"years_of_experience": "This field is required for professional users."})
            if not attrs.get('specialties'):
                raise serializers.ValidationError({"specialties": "This field is required for professional users."})
        
        return attrs

    def create(self, validated_data):
        # Remove profile-specific data
        user_type = validated_data.pop('user_type', 'amateur')
        years_of_experience = validated_data.pop('years_of_experience', None)
        specialties = validated_data.pop('specialties', '')
        portfolio_url = validated_data.pop('portfolio_url', '')
        interests = validated_data.pop('interests', [])
        address = validated_data.pop('address', '')
        profile_image = validated_data.pop('profile_image', None)
        Profile.objects.create(owner=user)
        
        # Remove password2 field
        validated_data.pop('password2', None)

        # Create user
        user = User.objects.create_user(**validated_data)

        # Create or update profile
        profile, _ = Profile.objects.update_or_create(
            owner=user,
            defaults={
                'user_type': user_type,
                'years_of_experience': years_of_experience,
                'specialties': specialties,
                'portfolio_url': portfolio_url,
                'interests': interests,
                'address': address,
                'name': user.get_full_name(),
                'image': profile_image if profile_image else 'default_profile_azwy8y'
            }
        )

        # Generate token
        refresh = RefreshToken.for_user(user)

        return {
            'user': user,
            'profile': profile,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = super().to_representation(instance['user'])
        profile = ProfileSerializer(instance['profile']).data
        ret.update({
            'profile': profile,
            'refresh': instance['refresh'],
            'access': instance['access'],
        })
        return ret