from django import forms
from accounts.models import User


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("birth", "gender", "email")
