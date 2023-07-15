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
    context['post_form'] = PostCreationForm()
    context['posts'] = room.room_posts.all()
    
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


#POSTS
def create_post(request,roomid):
    room = Room.objects.get(id=roomid)
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.room = room
            post.save()
            return HttpResponseRedirect(reverse('view_room',args=(roomid,)))
        else:
            return render(request, 'base/create_post.html', {'form': form,'room':room,'post':post})
    else:
        form = PostCreationForm(instance = form)
        return render(request, 'base/create_post.html', {'form': form,'room':room,'post':post})
    
def view_post(request,postid):
    post = get_object_or_404(Post, pk=postid)
    return render(request, 'base/view_post.html', {'post': post})

def delete_post(request,postid):
    post = Post.objects.get(id=postid)
    if request.method == 'POST':
        if post.creator.id == request.user.id:
            post.delete()
        else:
            return HttpResponse("Action not allowed")
        return HttpResponseRedirect(reverse('view_room',args=(post.room.id,)))
    else:
        return render(request, 'base/delete_post.html', {'post': post})

def update_post(request,postid):
    post = get_object_or_404(Post, pk=postid)
    if request.method == 'POST':
        form = PostCreationForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_room',args=(post.room.id,)))
        else:
            return render(request, 'base/update_post.html', {'post_form': form,'post': post})
    else:
        form = PostCreationForm(instance=post)
        return render(request, 'base/update_post.html', {'post_form': form,'post': post})