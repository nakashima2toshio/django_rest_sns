from django.db import models
from api.models import CustomUser
from django.contrib.auth import get_user_model

"""
Profile
custom_user: 1対1リレーション。CustomUserとProfileが1対1の関係で紐づいています。
CustomUserが削除されると、関連するProfileも削除されます。

Post
custom_user: 外部キー（Foreign Key）リレーション。
CustomUserとPostが多対1の関係で紐づいています。CustomUserが削除されると、関連するPostも削除されます。

Like
custom_user: 外部キー（Foreign Key）リレーション。
CustomUserとLikeが多対1の関係で紐づいています。CustomUserが削除されると、関連するLikeも削除されます。
post: 外部キー（Foreign Key）リレーション。PostとLikeが多対1の関係で紐づいています。
Postが削除されると、関連するLikeも削除されます。

Comment
custom_user: 外部キー（Foreign Key）リレーション。
CustomUserとCommentが多対1の関係で紐づいています。
CustomUserが削除されると、関連するCommentも削除されます。
post: 外部キー（Foreign Key）リレーション。
PostとCommentが多対1の関係で紐づいています。
Postが削除されると、関連するCommentも削除されます。

Follow
follower: 外部キー（Foreign Key）リレーション。
CustomUser（フォローする側）とFollowが多対1の関係で紐づいています。
CustomUserが削除されると、関連するFollowも削除されます。
followed: 外部キー（Foreign Key）リレーション。
CustomUser（フォローされる側）とFollowが多対1の関係で紐づいています。
CustomUserが削除されると、関連するFollowも削除されます。
"""


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
