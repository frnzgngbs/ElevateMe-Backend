from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework import viewsets

from ..Serializer.UserSerializer import UserSerializer


class UserView(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Handle business logic
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return super().create(request, *args, **kwargs)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
