from django.db import models
from accounts.models import Profile
import uuid

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
    # attachments = models.ManyToManyField("feed.PostMedia", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'@{self.user_id.username} posted on {self.created_at}'

class PostMedia(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    image = models.ImageField(upload_to='posts/')
    url = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Media for {self.post_id.user_id.username}\'s Post'

class Comment(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'@{self.user_id.username} commented to {self.post_id.user_id.username}\'s Post'

class Reaction(models.Model):
    REACTION_CHOICES = (
        ('like', '👍'),
        ('love', '❤'),
        ('insightful', '💡'),
    )
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    reaction = models.CharField(max_length=255, choices=REACTION_CHOICES, default="like")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'@{self.user_id.username} reacted {self.reaction} to {self.post_id.user_id.username}\'s Post'
