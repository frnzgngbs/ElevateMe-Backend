
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    date_joined = models.DateTimeField(default=timezone.now)

    STUDENT = "S"
    TEACHER = "T"

    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]

    user_type = models.CharField(max_length=1, choices=ROLE_CHOICES, default=STUDENT)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
