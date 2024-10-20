from pydantic import ValidationError
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.Model.ChannelSubmission import ChannelSubmission
from api.Model.RoomChannel import RoomChannel
from api.Serializer.ChannelSubmissionSerializer import ChannelSubmissionSerializer


class ChannelSubmissionView(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = ChannelSubmissionSerializer
    queryset = ChannelSubmission.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChannelSubmission.objects.filter(channel_id=self.kwargs['channel_pk'])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def submit(self, request, channel_pk=None):
        submitted_work = request.data.get('submitted_work')
        user_submitted = request.user

        serializer = self.get_serializer(data={
            "submitted_work": submitted_work,
            "member_id": user_submitted.id,
            "channel_id": channel_pk
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

