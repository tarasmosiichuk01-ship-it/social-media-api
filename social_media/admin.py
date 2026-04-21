from django.contrib import admin

from social_media.models import Post, Hashtag, Like, Comment

admin.register(Post)
admin.register(Hashtag)
admin.register(Like)
admin.register(Comment)
