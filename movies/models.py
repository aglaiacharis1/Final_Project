# movies/models.py

from django.conf import settings
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    release_year = models.IntegerField(verbose_name="Год выхода")
    poster = models.ImageField(
        upload_to="posters/", blank=True, null=True, verbose_name="Постер"
    )

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    imdb_id = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    poster = models.URLField(blank=True)
    year = models.CharField(max_length=10, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "imdb_id")
        ordering = ["-added"]

    def __str__(self):
        return f"{self.title} ({self.user})"