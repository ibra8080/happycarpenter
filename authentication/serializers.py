from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from profiles.models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    user_type = serializers.ChoiceField(choices=Profile.USER_TYPE_CHOICES, required=True)
    years_of_experience = serializers.IntegerField(required=False)
    specialties = serializers.CharField(required=False)
    portfolio_url = serializers.URLField(required=False)
    interests = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
    address = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name',
                  'user_type', 'years_of_experience', 'specialties', 'portfolio_url',
                  'interests', 'address')
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
        user_type = validated_data.pop('user_type')
        years_of_experience = validated_data.pop('years_of_experience', None)
        specialties = validated_data.pop('specialties', '')
        portfolio_url = validated_data.pop('portfolio_url', '')
        interests = validated_data.pop('interests', [])
        address = validated_data.pop('address', '')
        
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        
        Profile.objects.create(
            owner=user,
            user_type=user_type,
            years_of_experience=years_of_experience,
            specialties=specialties,
            portfolio_url=portfolio_url,
            interests=interests,
            address=address
        )
        
        return user