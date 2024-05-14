from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]

    def validate_password(self, data):
        if len(data.get('password')) < 6:
            raise serializers.ValidationError({'error': "Password must be at least of length 6."})
        return data

