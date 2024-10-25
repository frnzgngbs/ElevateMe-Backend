from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from api.Model.SubmissionVoting import SubmissionVotingMark
from api.Serializer.SubmissionVotingSerializer import SubmissionVotingMarkSerializer


class SubmissionVotingMarkView(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = SubmissionVotingMark.objects.all()
    serializer_class = SubmissionVotingMarkSerializer
    permission_classes = IsAuthenticated

    def get_queryset(self):
        submission_id = self.kwargs['submission_pk']
        return SubmissionVotingMark.objects.filter(submission_id=submission_id)


