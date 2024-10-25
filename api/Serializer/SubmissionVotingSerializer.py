from rest_framework import serializers

from api.Model.SubmissionVoting import SubmissionVotingMark


class SubmissionVotingMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionVotingMark
        fields = '__all__'