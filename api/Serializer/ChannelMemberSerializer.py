from rest_framework import serializers

from api.Model.ChannelMember import ChannelMember


class ChannelMemberSerializer(serializers.ModelSerializer):
    channel_members = serializers.ListField(
        child=serializers.EmailField(),
        required=False
    )

    class Meta:
        model = ChannelMember
        fields = '__all__'
