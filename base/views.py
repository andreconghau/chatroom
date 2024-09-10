from django.shortcuts import render, redirect
from django.http import HttpResponse

from base.forms import RoomForm
from .models import Room, Topic

# Create your views here.


def home(request):
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics}
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

def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    context = {'form': form}
    if request.method == 'POST':
        formData = RoomForm(request.POST, instance=room)
        if formData.is_valid():
            formData.save()
            print(f'Room {id} - {room.name} updated successfully')
            return redirect('home')
    return render(request, "base/pages/room_form.html", context)

def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    context = {'obj': room}
    if request.method == 'POST':
        room.delete()
        print(f'Room {id} - {room.name} deleted successfully')
        return redirect('home')
    return render(request, "base/pages/delete.html", context)
