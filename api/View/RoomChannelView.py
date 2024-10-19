from django.forms import model_to_dict
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from api.Model.ChannelMember import ChannelMember
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

    def get_serializer_class(self):
        if self.action == "members":
            return ChannelMemberSerializer
        return RoomChannelSerializer


    def get_object(self):
        if self.action == "members":
            channel = super().get_object()
            return ChannelMember.objects.filter(channel_id=channel.id)
        else:
            return super().get_object()

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

    def update(self, request, *args, **kwargs):
        channel = self.get_object()
        members_to_be_added = request.data.get('new_channel_member_emails', [])
        room_id = request.data.get('room_id')

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            raise ValidationError(f"Room with ID: {room_id} does not exist")


        print(model_to_dict(channel))
        print(members_to_be_added)

        for member_email in members_to_be_added:
            to_be_added = CustomUser.objects.get(email=member_email)

            try:
                to_be_added = CustomUser.objects.get(email=member_email)
            except CustomUser.DoesNotExist:
                raise ValidationError(f"User with email: {member_email} does not exist")

            print(model_to_dict(to_be_added))

            channel_member_data = {
                "room_id": room.id,
                "member_id": to_be_added.id,
                "channel_id": channel.id
            }

            print(channel_member_data)

            channel_member_serializer = ChannelMemberSerializer(data=channel_member_data)
            channel_member_serializer.is_valid(raise_exception=True)
            channel_member_serializer.save()

        return Response({"message": "Successfully added to the channel"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def members(self, request, pk):
        room_members = self.get_object()

        serializer = self.get_serializer(room_members, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['delete'], url_path='members/(?P<member_id>[^/.]+)')
    def remove_channel_member(self, request, pk, member_id):
        pass




