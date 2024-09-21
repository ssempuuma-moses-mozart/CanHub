from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import uuid
from datetime import datetime

# User = get_user_model()

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pic/')
    bio = models.TextField(max_length=160, blank=True, null=True)
    nickname = models.TextField(max_length=160, blank=True, null=True)
    location = models.TextField(max_length=160, blank=True, null=True)
    who = models.TextField(max_length=160, blank=True, null=True)
    gender = models.TextField(max_length=160, blank=True, null=True)
    age = models.TextField(max_length=160, blank=True, null=True)
    cancertype = models.TextField(max_length=160, blank=True, null=True)

    cover = models.ImageField(upload_to='covers/', blank=True)

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profile_pic": self.profile_pic.url,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

class Post(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    content_text = models.TextField(max_length=140, blank=True)
    content_image = models.ImageField(upload_to='posts/', blank=True)
    content_video = models.FileField(upload_to='posts/videos/', blank=True)  # Field for video uploads
    likers = models.ManyToManyField(User,blank=True , related_name='likes', null=True)
    savers = models.ManyToManyField(User,blank=True , related_name='saved', null=True)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post ID: {self.id} (creater: {self.creater})"

    def img_url(self):
        return self.content_image.url

    def append(self, name, value):
        self.name = value

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters', blank=True, null=True)
    comment_content = models.TextField(max_length=90, blank=True, null=True)
    comment_time = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"Post: {self.post} | Commenter: {self.commenter}"

    def serialize(self):
        return {
            "id": self.id,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }
    

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, null=True, blank=True)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('follower', 'followed')
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_follow'),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

    def clean(self):
        # Ensure a user cannot follow themselves
        if self.follower == self.followed:
            raise ValidationError("User cannot follow themselves.")
        

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100, null=True, blank=True)
    user = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'post')


class Group(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    
    GROUP_TYPE_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]
    
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Admin of the group
    group_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    rules = models.TextField(null=True, blank=True)
    group_type = models.CharField(max_length=7, choices=GROUP_TYPE_CHOICES, null=True, blank=True)
    cover_photo = models.ImageField(upload_to='group_covers/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='group_profiles/', blank=True, null=True)
    allow_invite = models.BooleanField(default=False, null=True, blank=True)
    post_review = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.group_name if self.group_name else "Unnamed Group"

class GroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'group')  # Ensure that a user can join a group only once

    def __str__(self):
        return f"{self.user.username} joined {self.group.group_name}"
    


class GroupPost(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_posts', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts', null=True)  # New ForeignKey
    date_created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    content_text = models.TextField(max_length=140, blank=True)
    content_image = models.ImageField(upload_to='group_posts/', blank=True)
    content_video = models.FileField(upload_to='group_posts/videos/', blank=True)  # Field for video uploads
    likers = models.ManyToManyField(User,blank=True , related_name='group_likes', null=True)
    savers = models.ManyToManyField(User,blank=True , related_name='group_saved', null=True)
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Post ID: {self.id} (creater: {self.creater})"

    def img_url(self):
        return self.content_image.url

    def append(self, name, value):
        self.name = value


class GroupComment(models.Model):
    group_post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='group_comments', blank=True, null=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_commenters', blank=True, null=True)
    comment_content = models.TextField(max_length=90, blank=True, null=True)
    comment_time = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"GroupPost: {self.group_post} | Commenter: {self.commenter}"

    def serialize(self):
        return {
            "id": self.id,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }        