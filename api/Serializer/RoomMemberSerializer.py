from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.Model.RoomMember import RoomMember


class RoomMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMember
        fields = '__all__'

    def validate(self, attrs):
        room_id = attrs.get('room_id')
        member_id = attrs.get('member_id')

        if RoomMember.objects.filter(room_id=room_id, member_id=member_id).exists():
            raise ValidationError(f'This member is already in the room.')

        return attrs
