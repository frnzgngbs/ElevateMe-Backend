from django.db import models

from api.Model.CustomUser import CustomUser
from api.Model.Room import Room


class RoomMember(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    member_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f''