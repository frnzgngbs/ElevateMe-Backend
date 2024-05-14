from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]

class ThreeVennSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.CharField()
    field3 = serializers.CharField()
    filter_field = serializers.CharField(required=False)

class TwoVennSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.CharField()
    filter_field = serializers.CharField(required=False)