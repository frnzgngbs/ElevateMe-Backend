from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from api.Model.CustomUser import CustomUser
from api.Model.Room import Room
from api.Serializer.RoomMemberSerializer import RoomMemberSerializer
from api.Serializer.RoomSerializer import RoomSerializer

class RoomView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

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

        room_serializer = self.get_serializer(data={"room_name": room_name, "room_owner_id": room_owner})
        room_serializer.is_valid(raise_exception=True)

        users = []
        for email in members_data:
            try:
                user = CustomUser.objects.get(email=email)
                users.append(user)
            except CustomUser.DoesNotExist:
                raise ValidationError(f"User with email {email} does not exist.")

        room = room_serializer.save(room_owner_id=room_owner)

        for user in users:
            room_member_data = {
                'room': room.pk,
                'member_id': user.pk
            }

            room_member_serializer = RoomMemberSerializer(data=room_member_data)
            if room_member_serializer.is_valid():
                room_member_serializer.save()
            else:
                raise ValidationError(room_member_serializer.errors)

        return Response(room_serializer.data, status=status.HTTP_201_CREATED)