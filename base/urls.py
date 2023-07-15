from django.urls import path,include
from .views import *

urlpatterns = [
    path('',index,name='index'),

    #profile
    path('accounts/<uuid:userid>',show_profile,name='profile'),
    
    #Rooms
    path('room/<int:roomid>',view_room,name='view_room'),
    path('room/<int:roomid>/delete',delete_room,name='delete_room'),
    path('create_room',create_room,name='create_room'),
    path('room/<int:roomid>/update',update_room,name='update_room'),

    
]
