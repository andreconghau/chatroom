from django.shortcuts import render, redirect
from django.http import HttpResponse

from base.forms import RoomForm
from .models import Room

# Create your views here.

rooms = [
    {'id': 1, "name": "Room 1", "status": "Available"},
    {'id': 2, "name": "Room 2", "status": "Available"},
    {'id': 3, "name": "Room 3", "status": "Unavailable"},
]

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, "base/pages/index.html", context)

def room(request, id):
    id_parse = int(id)
    room_item = Room.objects.get(id=id_parse)
    context = {'id': id_parse, 'room': room_item}  
    print(context)
    return render(request, "base/pages/room.html", context)

def createRoom(request):
    form = RoomForm()
    context = {'form': form}
    if request.method == 'POST':
        reqData = request.POST
        print(reqData)
        print(request.POST.get('name'))
        formData = RoomForm(request.POST)
        if formData.is_valid():
            formData.save()
            print('Room save successfully')
            return redirect('home')
        
    return render(request, "base/pages/room_form.html", context)


def get_room_by_id(room_id):
    for room in rooms:
        if room['id'] == room_id:
            return room
    return None