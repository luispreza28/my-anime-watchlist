from django.contrib import admin
from .models import User, Anime, UserAnimeList, Genre

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ("username", "email", "first_name", "last_name")

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
  list_display = ("title",)
  filter_horizontal = ('genre',)

@admin.register(UserAnimeList)
class UserAnimeListAdmin(admin.ModelAdmin):
  list_display = ("anime",)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
  list_display = ("name",)
