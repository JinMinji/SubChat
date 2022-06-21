from django import forms
# from django.db import models
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "contents")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("contents",)


