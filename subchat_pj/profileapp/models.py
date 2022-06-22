from django.db import models
# Create your tests here.


class Emoji(models.Model):
    emoji_name = models.CharField(max_length=10)

    def __str__(self):
        return self.emoji_name