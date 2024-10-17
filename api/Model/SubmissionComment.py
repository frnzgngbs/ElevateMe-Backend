from django.db import models

from api.Model.ChannelSubmission import ChannelSubmission
from api.Model.Comment import Comment
from api.Model.CustomUser import CustomUser


class SubmissionComment(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)  # Reference on what comment
    submission_id = models.ForeignKey(ChannelSubmission, on_delete=models.CASCADE)  # Reference on what work
    member_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Reference on who commented

    def __str__(self):
        return f'{self.comment_id.content} by {self.member_id.email}'