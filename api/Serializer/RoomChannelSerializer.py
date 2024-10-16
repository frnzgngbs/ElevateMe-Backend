from rest_framework import serializers

from api.Model.RoomChannel import RoomChannel


class RoomChannelSerializer(serializers.ModelSerializer):
    channel_members = serializers.ListSerializer(
        child=serializers.EmailField(),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = RoomChannel
        fields = '__all__'