from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('mypage/', views.mypage, name="mypage"),
    path('emoji/', views.emoji, name="emoji"),
    path('emoji_modify/<str:new_emoji_id>/', views.emoji_modify, name="emoji_modify"),
    path('change_password/', views.change_password, name="change_password"),
    path('test/', views.test),
]