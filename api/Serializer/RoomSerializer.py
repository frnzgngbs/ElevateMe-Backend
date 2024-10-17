from rest_framework import serializers

from api.Model.Room import Room
from api.Serializer.RoomMemberSerializer import RoomMemberSerializer


class RoomSerializer(serializers.ModelSerializer):
    new_room_member_emails = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=False
    )

    room_members = RoomMemberSerializer(source='roommember_set', many=True, read_only=True)
    class Meta:
        model = Room
        fields = '__all__'

    # def create(self, validated_data):
    #     members_data = validated_data.pop('members', [])
    #
    #     room = Room.objects.create(**validated_data)
    #
    #     for email in members_data:
    #
    #         try:
    #             user = CustomUser.objects.get(email=email)
    #         except CustomUser.DoesNotExist:
    #             raise serializers.ValidationError(f"User with email {email} does not exist.")
    #
    #         room_member_data = {
    #             'room': room.pk,
    #             'member_id': user.pk
    #         }
    #
    #         room_member_serializer = RoomMemberSerializer(data=room_member_data)
    #         if room_member_serializer.is_valid():
    #             room_member_serializer.save()
    #         else:
    #             raise serializers.ValidationError(room_member_serializer.errors)
    #
    #     return room

