from django.db import models

from api.Model.RoomChannel import RoomChannel
from api.Model.CustomUser import CustomUser

class ChannelSubmission(models.Model):
    submitted_work = models.TextField()  # TextField for now
    date_submitted = models.DateTimeField(auto_now_add=True)
    member_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Kinsa na user ang ni submit
    channel_id = models.ForeignKey(RoomChannel, on_delete=models.CASCADE)  # Diin nga channel ni submit

    class Meta:
        unique_together = ('member_id', 'channel_id')

    def __str__(self):
        return f'Submission by {self.member_id.first_name} in {self.channel_id.channel_name} on {self.date_submitted}'
