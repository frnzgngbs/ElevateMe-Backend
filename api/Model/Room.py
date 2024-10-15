from django.db import models

from api.Model.CustomUser import CustomUser


class Room(models.Model):
    room_name = models.TextField()
    room_owner_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.room_name}'