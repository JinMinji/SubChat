from django.shortcuts import render, redirect
from chatapp.models import Room


def main(request):
    rooms = Room.objects.all()
    return render(request, 'main/main.html', {'rooms': rooms})