from django.shortcuts import render, redirect
from django.db.models import Q
from base.forms import RoomForm
from .models import Room, Topic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.


def home(request):
    topic_id = request.GET.get('topic', None)
    search_param = request.GET.get('search', None)
    print(f'search_param: {search_param}')
    topics = Topic.objects.all()
    rooms_count = Room.objects.count()
    # Apply filters if topic_id or room_title is provided
    if topic_id or search_param:
        rooms = Room.objects.filter(
            Q(topic__id=topic_id) if topic_id else Q() |
            Q(name__icontains=search_param) | Q(description__icontains=search_param) if search_param else Q()
        )
    else:
        # If no filters are provided, return all rooms
        rooms = Room.objects.all()

    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count}
    return render(request, "base/pages/index.html", context)

def room(request, id):
    id_parse = int(id)
    room_item = Room.objects.get(id=id_parse)
    context = {'id': id_parse, 'room': room_item}  
    print(context)
    return render(request, "base/pages/room.html", context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!', status=401)
    form = RoomForm(instance=room)
    context = {'form': form}
    if request.method == 'POST':
        formData = RoomForm(request.POST, instance=room)
        if formData.is_valid():
            formData.save()
            print(f'Room {id} - {room.name} updated successfully')
            return redirect('home')
    return render(request, "base/pages/room_form.html", context)

@login_required(login_url='login')
def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!', status=401)
    context = {'obj': room}
    if request.method == 'POST':
        room.delete()
        print(f'Room {id} - {room.name} deleted successfully')
        return redirect('home')
    return render(request, "base/pages/delete.html", context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'Username: {username}, Password: {password}')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
        # if user.check_password(password):
        #     print('User authenticated')
        #     return redirect('home')
        # else:
        #     print('Password incorrect')
        #     messages.error(request, 'Authentication failed')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('User authenticated')
            return redirect('home')
        else:
            messages.error(request, 'Username or Passowrd is incorrect')
    context = {}

    return render(request, "base/pages/login.html", context)

def logoutPage(request):
    logout(request)
    return redirect('home')