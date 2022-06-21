from django.shortcuts import render, redirect
from chatapp.models import Room


def main(request):
    rooms = Room.objects.all()
    return render(request, 'chatapp/main.html', {'rooms': rooms})