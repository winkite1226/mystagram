from django.contrib import admin
from .models import Post, Comment, Bookmark, Like

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Bookmark)
admin.site.register(Like)
