from django import forms
# from django.db import models
from .models import Post, Comment
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    contents = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Post
        fields = ("title", "contents", "line")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("contents",)


