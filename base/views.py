from django.shortcuts import render,HttpResponse, HttpResponseRedirect,get_object_or_404
from django.urls import reverse
from .models import Room
from accounts.models import Account
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.encoding import smart_str
# Create your views here.

def index(request):
    context = {}
    rooms = ''
    if request.GET:
        t = request.GET.get('t')
        s = request.GET.get('s')
        if t:
            rooms = Room.objects.filter(Q(topic__name__icontains = t)).exclude(is_private = True)
        elif s:
            if s.startswith('@'):
                try:
                    user = Account.objects.get(username = s[1:])
                except:
                    return HttpResponse("<h1>USER NOT FOUND</h1>",status = 404)
                return HttpResponseRedirect(reverse('profile', args=(user.id,)))
            else:
                rooms = Room.objects.filter(Q(name__icontains = s))
    else:
        rooms = Room.objects.all().exclude(is_private=True)
    context['rooms'] = rooms
    context['creation_form'] = RoomCreationForm()
    context['file_form'] = RoomFileForm()
    context['topics'] = Topic.objects.all()
    
    return render(request,"index.html",context)

def show_profile(request,userid):
    context = {}
    context['requested_user'] = Account.objects.get(id=userid)   
    return render(request,"accounts/profile.html",context)

def get_room_file(request,fileid):
    file = get_object_or_404(RoomFile,pk=fileid)
    file_name = file.file.name
    response = HttpResponse(content_type = 'application/force-download') # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    response['X-Sendfile'] = smart_str(file.file.path)
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
    return

def get_post_file(request,fileid):
    file = get_object_or_404(PostFile,pk=fileid)
    file_name = file.file.name
    response = HttpResponse(content_type = 'application/force-download') # mimetype is replaced by content_type for django 1.7
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    response['X-Sendfile'] = smart_str(file.file.path)
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response
    return

#ROOMS

def view_room(request, roomid):
    context = {}
    room = Room.objects.get(id=roomid)
    context['room'] = room
    context['post_form'] = PostCreationForm()
    context['file_form'] = PostFileForm()
    context['posts'] = room.room_posts.all()
    context['joined'] = (request.user in room.participants.all())
    
    return render(request,"base/view_room.html",context)

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomCreationForm(request.POST)
        file_form = RoomFileForm(request.POST,request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid() and file_form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.save()
            room.participants.add(request.user)
            room.admins.add(request.user)
            for f in files:
                file_instance = RoomFile(file=f,room=room)
                file_instance.save()
            return HttpResponseRedirect(reverse('view_room',args=(room.id,)))
        else:
            return  render(request, 'base/create_room.html', {'form': form,'file_form':file_form,})
    else:
        form = RoomCreationForm()
        file_form = RoomFileForm(request.POST,request.FILES)
        return render(request, 'base/create_room.html', {'form': form,'file_form':file_form})
    
@login_required
def update_room(request,roomid):
    room = get_object_or_404(Room, pk=roomid)
    if request.method == 'POST':
        form = RoomCreationForm(request.POST,instance = room)
        file_form = RoomFileForm(request.POST,request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid() and file_form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.save()
            room.participants.add(request.user)
            room.admins.add(request.user)
            for f in files:
                file_instance = RoomFile(file=f,room=room)
                file_instance.save()
            return HttpResponseRedirect(reverse('view_room',args=(room.id,)))
    else:
        form = RoomCreationForm(instance=room)
        file_form = RoomFileForm(request.POST,request.FILES)
        return render(request, 'base/update_room.html', {'form': form,'file_form':file_form,'room': room})
    
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
    if request.user == room.creator:
        return HttpResponse("<h1>Creator cannot leave room</h1>")
    room.participants.remove(request.user)
    return HttpResponseRedirect(reverse('view_room', args=(roomid,)))

#POSTS
@login_required
def create_post(request,roomid):
    context = {}
    room = Room.objects.get(id=roomid)
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        file_form = PostFileForm(request.POST,request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid() and file_form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.room = room
            post.save()
            for f in files:
                file_instance = PostFile(file=f,post=post)
                file_instance.save()
            return HttpResponseRedirect(reverse('view_post',args=(post.id,)))
        else:
            return render(request, 'base/create_post.html', {'form': form,'file_form':file_form,'room':room,'post':post})
    else:
        form = PostCreationForm(instance = form)
        file_form = PostFileForm(request.POST,request.FILES)
        context['form'] = form
        context['file_form'] = file_form
        context['room'] = room
        context['post'] = post
        return render(request, 'base/create_post.html', context)
    
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
        file_form = PostFileForm(request.POST,request.FILES)
        files = request.POST.getlist('file')
        if form.is_valid() and file_form.is_valid():
            form.save()
            for f in files:
                file_instance = PostFile(file=f,post=post)
                file_instance.save()
            return HttpResponseRedirect(reverse('view_post',args=(post.id,)))
        else:
            return render(request, 'base/update_post.html', {'post_form': form,'post': post})
    else:
        context = {}
        form = PostCreationForm(instance=post)
        file_form = PostFileForm(request.POST,request.FILES)
        context['post_form'] = form
        context['file_form'] = file_form
        context['post'] = post
        return render(request, 'base/update_post.html', context)
    


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

