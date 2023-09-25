from rest_framework import serializers
from api.models import Users


class OnlineUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'private_channel_name']