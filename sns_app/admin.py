from django.contrib import admin
from sns_app.models import Profile, Post, Like, Comment, Follow

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
