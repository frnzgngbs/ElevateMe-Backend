from rest_framework import status, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound


from api.Model.RoomChannel import RoomChannel
from api.Serializer.RoomChannelSerializer import RoomChannelSerializer


class RoomChannelView(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = RoomChannel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RoomChannelSerializer