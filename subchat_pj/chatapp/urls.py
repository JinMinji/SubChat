from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.main, name="main"),
    path("rooms/", views.rooms, name= "rooms"),
    path('<slug:slug>/', views.room, name='room'),
]
