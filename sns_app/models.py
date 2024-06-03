from django.db import models
from api.models import CustomUser
from django.contrib.auth import get_user_model


class Profile(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True, null=True)


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    custom_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # 追加
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
