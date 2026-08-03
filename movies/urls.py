# movies/urls.py

from django.urls import path

from .views import (
    AboutPageView,
    add_favorite,
    catalog,
    favorites,
    home,
    movie_detail,
    remove_favorite,
    search,
)

urlpatterns = [
    path("", home, name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("search/", search, name="search"),
    path("catalog/", catalog, name="catalog"),
    path("favorites/", favorites, name="favorites"),
    path("movie/<str:imdb_id>/", movie_detail, name="movie_detail"),
    path("favorites/add/<str:imdb_id>/", add_favorite, name="add_favorite"),
    path("favorites/remove/<int:pk>/", remove_favorite, name="remove_favorite"),
]