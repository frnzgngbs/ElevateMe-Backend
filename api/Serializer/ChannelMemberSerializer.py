from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.Model.ChannelMember import ChannelMember


class ChannelMemberSerializer(serializers.ModelSerializer):
    channel_members = serializers.ListField(
        child=serializers.EmailField(),
        required=False
    )

    class Meta:
        model = ChannelMember
        fields = '__all__'


    def validate(self, attrs):
        channel_id = attrs.get('channel_id')
        member_id = attrs.get('member_id')

        if ChannelMember.objects.filter(channel_id=channel_id, member_id=member_id).exists():
            raise ValidationError(f'This member is already in the channel.')

        return attrs
