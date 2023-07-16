from django.db import models
from accounts.models import Account
from django.db import models

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=120)
    description = MarkdownField(rendered_field='description_rendered', validator=VALIDATOR_STANDARD)
    description_rendered = RenderedMarkdownField()
    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    topic = models.ForeignKey(Topic,null=True, on_delete=models.SET_NULL ,related_name='topic_rooms')
    
    creator = models.ForeignKey(Account,null=True,on_delete=models.SET_NULL,related_name='created_rooms')
    admins = models.ManyToManyField(Account,related_name='administrated_rooms')
    participants = models.ManyToManyField(Account,related_name='joined_rooms')
    
    def get_participant_count(self):
        return self.participants.all().count()
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name 
    
class RoomFile(models.Model):
    file = models.FileField(upload_to='./room_files/',null=True,blank=True,)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_files')
    
    class Meta:
        unique_together = ('file', 'room')

    def __str__(self): 
        return self.file.name

class Post(models.Model):
    title = models.CharField(max_length=120)
    content = MarkdownField(rendered_field='content_rendered', validator=VALIDATOR_STANDARD)
    content_rendered = RenderedMarkdownField()

    creator = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="user_posts")
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='room_posts')
    likes = models.ManyToManyField(Account,related_name='liked_posts')
    dislikes = models.ManyToManyField(Account,related_name='disliked_posts')
    bookmarks = models.ManyToManyField(Account,related_name='bookmarked_posts')
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pinned','-created_at']

    def __str__(self):
        return self.title
    
class PostFile(models.Model):
    file = models.FileField(upload_to='./post_files/',null=True,blank=True,)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_files')

    class Meta:
        unique_together = ('file', 'post')  

    def __str__(self):
        return self.file.name
    

class Comment(models.Model):
    creator = models.ForeignKey(Account,on_delete=models.CASCADE ,related_name='user_comments')
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False)
    likes = models.ManyToManyField(Account,related_name='liked_comments')
    dislikes = models.ManyToManyField(Account,related_name='disliked_comments')

    class Meta:
        ordering = ['pinned','-created_at']
    
    def __str__(self):
        return self.creator +' '+ self.content[:50] + '...'
    
