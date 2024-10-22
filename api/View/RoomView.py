from django.forms import model_to_dict
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from api.Model.CustomUser import CustomUser
from api.Model.Room import Room
from api.Model.RoomChannel import RoomChannel
from api.Model.RoomMember import RoomMember
from api.Serializer.RoomChannelSerializer import RoomChannelSerializer
from api.Serializer.RoomMemberSerializer import RoomMemberSerializer, RoomMemberDeletionSerializer
from api.Serializer.RoomSerializer import RoomSerializer, RoomJoinSerializer

class RoomView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if (self.action == "members" or
            self.action == "auth_rooms"):
            return RoomMemberSerializer
        elif self.action == "channels":
            return RoomChannelSerializer
        elif self.action == "remove_room_member":
            return RoomMemberDeletionSerializer
        elif self.action == "join":
            return RoomJoinSerializer
        return RoomSerializer
    def get_object(self):
        if self.action == "members":
            room = super().get_object()
            return RoomMember.objects.filter(room_id=room.id)
        else:
            return super().get_object()

    def create(self, request, *args, **kwargs):
        """
            Payload to create a room
            {
                members: list[]
                room_name: string,
            }
        """
        members_data = request.data.get('new_room_member_emails', [])
        room_name = request.data.get('room_name')

        room_owner = CustomUser.objects.filter(email=request.user).first()

        room_serializer = self.get_serializer(data={"room_name": room_name, "room_owner_id": room_owner.id})
        room_serializer.is_valid(raise_exception=True)

        users = []
        users.append(room_owner)
        for email in members_data:
            try:
                user = CustomUser.objects.get(email=email)
                users.append(user)
            except CustomUser.DoesNotExist:
                raise ValidationError(f"User with email {email} does not exist.")

        room = room_serializer.save()

        for user in users:
            room_member_data = {
                'room_id': room.pk,
                'member_id': user.pk
            }

            room_member_serializer = RoomMemberSerializer(data=room_member_data)
            room_member_serializer.is_valid(raise_exception=True)
            room_member_serializer.save()

        return Response(room_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        room = self.get_object()
        members_to_be_added = request.data.get('new_room_members', [])

        print(model_to_dict(room))
        for member_email in members_to_be_added:
            try:
                to_be_added = CustomUser.objects.get(email=member_email)
            except CustomUser.DoesNotExist:
                raise ValidationError(f"User with email: {member_email} does not exist")

            print(model_to_dict(to_be_added))

            room_member_data = {
                "room_id": room.id,
                "member_id": to_be_added.id
            }

            room_member_serializer = RoomMemberSerializer(data=room_member_data)
            room_member_serializer.is_valid(raise_exception=True)
            room_member_serializer.save()

        return Response({"message": "Successfully added to the room"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def members(self, request, pk):
        room_members = self.get_object()
        if request.method == "GET":
            serializer = self.get_serializer(room_members, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def channels(self, request, pk):
        room = self.get_object()

        channels = RoomChannel.objects.filter(room_id=room.id)

        serializer = self.get_serializer(channels, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='members/(?P<member_id>[^/.]+)')
    def remove_room_member(self, request, pk, member_id):
        serializer = self.get_serializer(data={'room_id': pk, 'member_id': member_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def join(self, request):
        room_code = request.data.get('room_code')
        member_id = request.data.get('member_id')

        serializer = self.get_serializer(data={"room_code": room_code, "member_id": member_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def auth_rooms(self, request):
        user = request.user

        room_members = RoomMember.objects.filter(member_id=user.id)

        room_member_serializer = RoomMemberSerializer(room_members, many=True)

        room_ids = set()

        for room_member in room_member_serializer.data:
            room_ids.add(room_member['room_id'])

        rooms = Room.objects.filter(id__in=room_ids)

        room_serializer = RoomSerializer(rooms, many=True)

        return Response(room_serializer.data, status=status.HTTP_200_OK)


    # def destroy(self, request, *args, **kwargs):
    #     print(kwargs.get('pk'))
    #
    #     room_id = kwargs.get('pk')
    #
    #     """
    #         STEP 1: Get rooms
    #         STEP 2: Get Channel
    #         STEP 3: Get Channel Members and Delete
    #         STEP 4: Delete Channels
    #         STEP 5: Delete Room
    #     """
    #
    #     try:
    #         with transaction.atomic():
    #             room = self.get_queryset().get(id=room_id)
    #
    #
    #     except Room.DoesNotExist:
    #         raise ValidationError({"error": f"Room with id {room_id} does not exist"})
    #
    #     return None

