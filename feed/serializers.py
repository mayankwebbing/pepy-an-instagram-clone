from rest_framework import serializers
from accounts.models import Profile

class ProfileBasicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'full_name', 'profile_img']