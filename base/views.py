from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

rooms = [
    {'id': 1, "name": "Room 1", "status": "Available"},
    {'id': 2, "name": "Room 2", "status": "Available"},
    {'id': 3, "name": "Room 3", "status": "Unavailable"},
]

def home(request):
    context = {'rooms': rooms}
    return render(request, "base/pages/index.html", context)

def room(request, id):
    id_parse = int(id)
    room_item = get_room_by_id(id_parse)
    context = {'id': id_parse, 'room': room_item}  
    print(context)
    return render(request, "base/pages/room.html", context)


def get_room_by_id(room_id):
    for room in rooms:
        if room['id'] == room_id:
            return room
    return None