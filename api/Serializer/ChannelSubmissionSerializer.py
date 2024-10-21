from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.Model.ChannelMember import ChannelMember
from api.Model.ChannelSubmission import ChannelSubmission
from api.Model.CustomUser import CustomUser
from api.Model.RoomChannel import RoomChannel

class ChannelSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelSubmission
        fields = '__all__'

    def validate(self, attrs):
        channel = attrs.get('channel_id')
        member = attrs.get('member_id')

        try:
            channel = RoomChannel.objects.get(id=channel.id)
        except RoomChannel.DoesNotExist:
            raise ValidationError(f"Channel with channel_id: {channel.id} does not exist")

        try:
            member = CustomUser.objects.get(id=member.id)
        except CustomUser.DoesNotExist:
            raise ValidationError(f"User with member_id: {member.id} does not exist")

        if not ChannelMember.objects.filter(member_id=member.id, channel_id=channel.id).exists():
            raise ValidationError(f"Member with member_id: {member.id} does not exist in channel with channel_id: {channel.id}")

        if ChannelSubmission.objects.filter(channel_id=channel.id, member_id=member.id).exists():
            raise ValidationError(f"Member with member_id: {member.id} has already submitted in channel with channel_id: {channel.id}")

        return attrs
