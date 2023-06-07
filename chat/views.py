from django.shortcuts import render

from chat.models import Room


def index_view(request):
    return render(request, 'chats/index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'chats/room.html', {
        'room': chat_room,
    })