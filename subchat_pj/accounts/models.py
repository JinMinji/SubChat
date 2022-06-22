from django.db import models
from django.contrib.auth.models import AbstractUser


class Emoji(models.Model):
    emoji_name = models.CharField(max_length=10)

    def __str__(self):
        return self.emoji_name


class User(AbstractUser):
    birth = models.CharField(max_length=15)
    gender = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    emoji = models.ForeignKey(Emoji, on_delete=models.SET_NULL, null=True)



