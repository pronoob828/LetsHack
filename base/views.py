from django.shortcuts import render,HttpResponse
from .models import Room
from accounts.models import Account

# Create your views here.

def index(request):
    context = {}
    rooms = Room.objects.all()
    context['rooms'] = rooms
    
    return render(request,"index.html",context)

def show_profile(request,userid):
    context = {}
    context['requested_user'] = Account.objects.get(id=userid)   
    return render(request,"accounts/profile.html",context)

def view_room(request, roomid):
    context = {}
    room = Room.objects.get(id=roomid)
    context['room'] = room
    
    return render(request,"base/view_room.html",context)