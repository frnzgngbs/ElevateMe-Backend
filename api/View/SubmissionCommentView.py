from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.Model.Comment import Comment
from api.Model.SubmissionComment import SubmissionComment
from api.Serializer.CommentSerializer import CommentSerializer
from api.Serializer.SubmissionCommentSerializer import SubmissionCommentSerializer


class SubmissionCommentView(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return SubmissionCommentSerializer
        return self.serializer_class

    def get_queryset(self):
        submission_id = self.kwargs['submission_pk']
        return SubmissionComment.objects.filter(comment_id__submission_id=submission_id)


    def create(self, request, *args, **kwargs):
        submission_id = kwargs.get('submission_pk')
        content = request.data.get('content')

        serializer = self.get_serializer(data={
            "content": content,
            "submission_id": submission_id,
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Commented successfully"}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SubmissionCommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)