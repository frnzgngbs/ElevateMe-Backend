from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from ..Serializer.UserSerializer import UserSerializer


class UserView(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."})

        user = authenticate(username=username, password=password)

        if user is None:
            print(f"Authentication failed for user: {username}")
            return Response({"error": "Invalid credentials."})

        # Check if the user account is active
        if not user.is_active:
            return Response({"error": "User account is inactive."})

        token = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


