from django.contrib import admin
from .models import Recipe, Like, Comment

admin.site.register(Recipe)
admin.site.register(Like)
admin.site.register(Comment)