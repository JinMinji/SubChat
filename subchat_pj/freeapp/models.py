from django.db import models
from accounts.models import User
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    reason_num = models.IntegerField(default=1)
    # ["욕설", "비방", "음란물", "기타"]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.contents


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Hate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
