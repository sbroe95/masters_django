from django.contrib import admin
from .models import Post
from users.models import PlayerChoices

admin.site.register(Post)
admin.site.register(PlayerChoices)