from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from profiles.serializers import ProfileSerializer

class CurrentUserSerializer(UserDetailsSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('profile',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        profile = instance.profile_set.first()
        if profile:
            representation['profile'] = ProfileSerializer(profile, context=self.context).data
        return representation