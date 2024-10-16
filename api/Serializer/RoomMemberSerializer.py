from rest_framework import serializers

from api.Model.RoomMember import RoomMember


class RoomMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMember
        fields = '__all__'

