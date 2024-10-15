from django.db import models

from api.Model.Room import Room


class RoomChannel(models.Model):
    channel_name = models.TextField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.channel_name} on {self.room_id.room_name} '
