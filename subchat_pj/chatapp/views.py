from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message, Room

def main(request):
    rooms = Room.objects.all()
    return render(request, 'main/main.html', {'rooms': rooms})

# Create your views here.
@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'main/main.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]
    return render(request, 'chatapp/room.html', {'room': room, 'messages': messages})

