from django.urls import path,include
from .views import *

urlpatterns = [
    path('',index,name='index'),

    #profile
    path('accounts/<uuid:userid>',show_profile,name='profile'),
    
    #Rooms
    path('room/<int:roomid>',view_room,name='view_room'),
    
]
