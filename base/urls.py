from django.urls import path,include
from .views import *

urlpatterns = [
    path('',index,name='index'),

    #profile
    path('accounts/<uuid:userid>',show_profile,name='profile'),
    
    #Rooms
    path('room/<int:roomid>',view_room,name='view_room'),
    path('create_room',create_room,name='create_room'),
    path('room/<int:roomid>/update',update_room,name='update_room'),
    path('room/<int:roomid>/delete',delete_room,name='delete_room'),

    #Posts
    path('create_post/<int:roomid>',create_post,name='create_post'),
    path('post/<int:postid>',view_post,name='view_post'),
    path('post/<int:postid>/delete',delete_post,name='delete_post'),
    path('post/<int:postid>/update',update_post,name='update_post'),

    
]
