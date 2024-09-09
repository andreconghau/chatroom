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
    return render(request, "pages/index.html", context)

def room(request):  
    return render(request, "room.html")

