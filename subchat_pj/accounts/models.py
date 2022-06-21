from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birth = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

