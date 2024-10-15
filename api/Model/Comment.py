from django.db import models

class Comment(models.Model):
    content = models.TextField()

    def __str__(self):
        return f'{self.content}'
