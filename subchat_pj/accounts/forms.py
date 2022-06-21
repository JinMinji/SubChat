from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    year = forms.CharField(label="년도")
    month = forms.CharField(label="월")
    day = forms.CharField(label="일")
    gender = forms.CharField(label="성별")
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "year", "month", "day", "gender", "email")
