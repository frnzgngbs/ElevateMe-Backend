from django.forms import model_to_dict
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from api.Model.CustomUser import CustomUser
from api.Model.Room import Room
from api.Model.RoomMember import RoomMember
from api.Serializer.RoomMemberSerializer import RoomMemberSerializer
from api.Serializer.RoomSerializer import RoomSerializer

class RoomView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "members":
            return RoomMemberSerializer
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
        members_data = request.data.get('members', [])
        room_name = request.data.get('room_name')

        room_owner = CustomUser.objects.filter(email=request.user).first()

        print(room_owner)

        room_serializer = self.get_serializer(data={"room_name": room_name, "room_owner_id": room_owner.id})
        room_serializer.is_valid(raise_exception=True)

        users = []
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
        members_to_be_added = request.data.get('room_members', [])

        print(model_to_dict(room))
        if room:
            for member in members_to_be_added:
                to_be_added = CustomUser.objects.get(email=member)

                print(model_to_dict(to_be_added))


                room_member_data = {
                    "room_id": room.id,
                    "member_id": to_be_added.id
                }

                room_member_serializer = RoomMemberSerializer(data=room_member_data)
                room_member_serializer.is_valid(raise_exception=True)
                room_member_serializer.save()

                return Response({"message": "Successfully added to the room"}, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError(f'Room with this id {pk} does not exist')


    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        room_members = self.get_object()

        serializer = self.get_serializer(room_members, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)