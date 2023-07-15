from django.shortcuts import render,HttpResponse, HttpResponseRedirect,get_object_or_404
from django.urls import reverse
from .models import Room
from accounts.models import Account
from .forms import *
from django.contrib.auth.decorators import login_required
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
    context['joined'] = (request.user in room.participants.all())
    
    return render(request,"base/view_room.html",context)

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.participants.add(request.user)
            room.admins.add(request.user)
            room.save()
            return HttpResponseRedirect(reverse('view_room',args=(room.id,)))
        else:
            return render(request, 'base/create_room.html', {'form': form})
    else:
        form = RoomCreationForm()
        return render(request, 'base/create_room.html', {'form': form})
    
@login_required
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
        form = RoomCreationForm()
        return render(request, 'base/update_room.html', {'form': form,'room': room})
    
@login_required
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

@login_required
def join_room(request,roomid):
    room = get_object_or_404(Room, pk=roomid)
    room.participants.add(request.user)
    return HttpResponseRedirect(reverse('view_room', args=(roomid,)))

@login_required
def leave_room(request,roomid):
    room = get_object_or_404(Room, pk=roomid)
    room.participants.remove(request.user)
    return HttpResponseRedirect(reverse('view_room', args=(roomid,)))

#POSTS
@login_required
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
    comments = post.post_comments.all()
    comment_form = CommentCreationForm()
    return render(request, 'base/view_post.html', {'post': post , 'comments': comments,'comment_form': comment_form})

@login_required
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

@login_required
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
        form = PostCreationForm()
        return render(request, 'base/update_post.html', {'post_form': form,'post': post})
    


#COMMENTS
@login_required
def create_comment(request,postid):
    post = get_object_or_404(Post, pk=postid)
    if request.method == 'POST':
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.creator = request.user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('view_post',args=(postid,)))
        else:
            return render(request, 'base/view_post.html', {'comment_form': form,'post':post,'comment':comment})
    else:
        form = CommentCreationForm()
        return render(request, 'base/view_post.html', {'comment_form': form,'post':post,'comment':comment})
    
@login_required
def delete_comment(request,commentid):
    comment = get_object_or_404(Comment, pk=commentid)
    if request.method == 'POST':
        if comment.creator.id == request.user.id:
            comment.delete()
        else:
            return HttpResponse("Action not allowed")
        return HttpResponseRedirect(reverse('view_post',args=(comment.post.id,)))
    else:
        return render(request, 'base/delete_comment.html', {'comment': comment})

