from rest_framework import serializers

from api.Model.CustomUser import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "user_type"]

    def validate_password(self, data):
        password = data
        if len(password) < 6:
            raise serializers.ValidationError({'error': "Password must be at least of length 6."})
        return data

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']