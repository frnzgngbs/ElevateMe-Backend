from django.db import models

from api.Model.ChannelSubmission import ChannelSubmission


class Comment(models.Model):
    content = models.TextField()
    commented_on = models.DateTimeField(auto_now_add=True)
    submission_id = models.ForeignKey(ChannelSubmission, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.content}'
