from rest_framework import serializers
from api.models import CustomUser
from api.serializers import ProfileSerializer
from .models import Post, Like, Comment, Follow, Profile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        ref_name = 'SNS_CustomUser'


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'custom_user', 'post', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'custom_user', 'post', 'content', 'created_at', 'updated_at']


class FollowSerializer(serializers.ModelSerializer):
    follower = CustomUserSerializer(read_only=True)
    followed = CustomUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'timestamp']


class ProfileSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['custom_user', 'display_name', 'bio']
        ref_name = 'SNSAppProfile'

