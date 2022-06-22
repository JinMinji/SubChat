from django.db import models
from django.contrib.auth.models import AbstractUser
from profileapp.models import Emoji
import datetime


class User(AbstractUser):
    birth = models.DateField(default=datetime.date.today())
    gender = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    emoji = models.ForeignKey(Emoji, on_delete=models.SET_NULL, null=True, default=1)



