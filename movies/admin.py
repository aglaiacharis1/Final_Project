from django.contrib import admin
from .models import Favorite, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year")
    search_fields = ("title",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "year", "added")
    list_filter = ("user",)
    search_fields = ("title", "imdb_id")


