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


    def create(self, request, *args, **kwargs):
        channel_members = request.data.get('channel_members')

    """
        Payload is the request.body from the front-end
        Payload in creating a room channel
        {
            channel_name: string,
            room_id: int,
            channel_members: list[] only members sa room
        }
    """