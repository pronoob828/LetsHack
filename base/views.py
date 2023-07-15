from django.shortcuts import render,HttpResponse, HttpResponseRedirect,get_object_or_404
from django.urls import reverse
from .models import Room
from accounts.models import Account
from .forms import *
# Create your views here.

def index(request):
    context = {}
    rooms = Room.objects.all()
    context['rooms'] = rooms
    context['creation_form'] = RoomCreationForm()
    
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

def create_room(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.save()
            return HttpResponseRedirect(reverse('view_room',args=(room.id,)))
        else:
            return render(request, 'base/create_room.html', {'form': form})
    else:
        form = RoomCreationForm(instance = form)
        return render(request, 'base/create_room.html', {'form': form})
    
def update_room(request,roomid):
    room = get_object_or_404(Room, pk=roomid)
    if request.method == 'POST':
        form = RoomCreationForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_room',args=(roomid,)))
        else:
            return render(request, 'base/update_room.html', {'form': form,'room': room})
    else:
        form = RoomCreationForm(instance=room)
        return render(request, 'base/update_room.html', {'form': form,'room': room})
    
def delete_room(request,roomid):
    room = Room.objects.get(id=roomid)
    if request.method == 'POST':
        if room.creator.id == request.user.id or request.user.id in room.admins.all():
            room.delete()
        else:
            return HttpResponse("Action not allowed")
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'base/delete_room.html', {'room': room})