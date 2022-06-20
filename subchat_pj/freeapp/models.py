from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now_add=True)
    report_cnt = models.IntegerField(default=0)
    line = models.IntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    view_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.contents

