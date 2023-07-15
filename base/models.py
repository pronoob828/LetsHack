from django.db import models
from accounts.models import Account

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
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
    

class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
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
    
