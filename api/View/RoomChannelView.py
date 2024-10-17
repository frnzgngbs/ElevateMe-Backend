from rest_framework import status, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from api.Model.CustomUser import CustomUser
from api.Model.Room import Room
from api.Model.RoomChannel import RoomChannel
from api.Serializer.ChannelMemberSerializer import ChannelMemberSerializer
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


    """
        Payload is the request.body from the front-end
        Payload in creating a room channel
        {
            channel_name: string,
            room_id: int,
            channel_members: list[] only members sa room
        }
    """

    def create(self, request, *args, **kwargs):
        print(request.data)
        channel_members = request.data.get('channel_members', [])
        channel_name = request.data.get('channel_name')
        room_id = request.data.get('room_id')

        room = Room.objects.filter(id=room_id).first()

        channel_serializer = self.get_serializer(data={"channel_name": channel_name, "room_id": room.id })
        channel_serializer.is_valid(raise_exception=True)

        members = []

        for email in channel_members:
            try:
                member = CustomUser.objects.get(email=email)
                members.append(member)
            except CustomUser.DoesNotExist:
                raise ValidationError(f'User with email {email} does not exist.')


        channel = channel_serializer.save()

        for member in members:
            channel_member_data = {
                "member_id": member.id,
                "channel_id": channel.id
            }

            channel_member_serializer = ChannelMemberSerializer(data=channel_member_data)
            channel_member_serializer.is_valid(raise_exception=True)
            channel_member_serializer.save()

        return Response(channel_serializer.data, status=status.HTTP_201_CREATED)



