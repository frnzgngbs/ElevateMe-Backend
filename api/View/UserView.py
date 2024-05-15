from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins

from ..Serializer.UserSerializer import UserSerializer


class UserView(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

