from django import forms
from accounts.models import User


class CustomUserChangeForm(forms.ModelForm):
    birth = forms.DateField(label="생년월일")
    gender = forms.CharField(label="성별")
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("birth", "gender", "email")
