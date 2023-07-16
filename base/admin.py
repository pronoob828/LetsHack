from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Room)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(PostFile)
admin.site.register(RoomFile)