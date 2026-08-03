# movies/views.py
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from .models import Favorite
from .omdb import get_details, search_by_genre_year, search_movies

# key -> (label, OMDb genre keyword, badge css class)
MOOD_MAP = {
    "laugh": ("I want to laugh 😂", "Comedy", "badge-comedy"),
    "thrill": ("I want a thrill 😱", "Horror", "badge-horror"),
    "think": ("I want to think 🤔", "Drama", "badge-drama"),
    "adrenaline": ("I want some adrenaline 💥", "Action", "badge-action"),
    "fairytale": ("I want a fairytale 🦄", "Fantasy", "badge-fantasy"),
    "love": ("I want to fall in love 💕", "Romance", "badge-romance"),
}


class AboutPageView(TemplateView):
    template_name = "movies/about.html"


def _favorite_ids(user):
    if not user.is_authenticated:
        return set()
    return set(Favorite.objects.filter(user=user).values_list("imdb_id", flat=True))


def home(request):
    """Mood generator: pick a random movie matching genre/year/rating filters.
    'Seen' titles and pick history live in the session, same idea as the
    original Streamlit prototype's session_state."""
    if request.method == "POST":
        mood_key = request.POST.get("mood", "laugh")
        year_from = int(request.POST.get("year_from", 2000))
        year_to = int(request.POST.get("year_to", 2024))
        if year_from > year_to:
            year_from, year_to = year_to, year_from
        min_rating = float(request.POST.get("min_rating", 5.0))

        seen_ids = request.session.get("seen_ids", [])
        history = request.session.get("history", [])

        _, genre, _ = MOOD_MAP.get(mood_key, MOOD_MAP["laugh"])
        year = random.randint(year_from, year_to)
        data = search_by_genre_year(genre, year)

        picked = None
        if data.get("Response") == "True":
            candidates = [m for m in data["Search"] if m["imdbID"] not in seen_ids]
            if not candidates:
                seen_ids = []
                candidates = data["Search"]
            random.shuffle(candidates)
            for candidate in candidates[:5]:
                details = get_details(candidate["imdbID"])
                try:
                    if float(details.get("imdbRating", 0)) >= min_rating:
                        candidate["imdbRating"] = details.get("imdbRating", "N/A")
                        picked = candidate
                        break
                except (ValueError, TypeError):
                    continue

        if picked:
            seen_ids.append(picked["imdbID"])
            history.append(picked)
            request.session["seen_ids"] = seen_ids
            request.session["history"] = history[-10:]
            request.session["last_found"] = picked
        else:
            request.session["last_found"] = None
            messages.warning(
                request,
                "No movies matched your filters — try lowering the rating or widening the year range.",
            )

        request.session["mood_key"] = mood_key
        request.session["year_from"] = year_from
        request.session["year_to"] = year_to
        request.session["min_rating"] = min_rating
        return redirect("home")

    mood_key = request.session.get("mood_key", "laugh")
    _, genre, badge_class = MOOD_MAP[mood_key]
    history = request.session.get("history", [])

    context = {
        "mood_map": MOOD_MAP,
        "selected_mood": mood_key,
        "genre": genre,
        "badge_class": badge_class,
        "year_from": request.session.get("year_from", 2000),
        "year_to": request.session.get("year_to", 2024),
        "min_rating": request.session.get("min_rating", 5.0),
        "last_found": request.session.get("last_found"),
        "history": list(reversed(history[:-1])) if history else [],
        "seen_count": len(request.session.get("seen_ids", [])),
        "favorite_ids": _favorite_ids(request.user),
    }
    return render(request, "movies/home.html", context)


def search(request):
    query = request.GET.get("q", "").strip()
    results = []
    error = None
    if query:
        if len(query) < 2:
            error = "Please enter at least 2 characters."
        else:
            data = search_movies(query)
            if data.get("Response") == "True":
                results = data["Search"]
            else:
                error = "Nothing found."

    return render(
        request,
        "movies/search.html",
        {
            "query": query,
            "results": results,
            "error": error,
            "favorite_ids": _favorite_ids(request.user),
        },
    )


def movie_detail(request, imdb_id):
    movie = get_details(imdb_id)
    trailer_url = None
    if movie.get("Title"):
        trailer_url = (
            "https://www.youtube.com/results?search_query="
            + movie["Title"].replace(" ", "+")
            + "+official+trailer"
        )
    return render(
        request,
        "movies/movie_detail.html",
        {
            "movie": movie,
            "trailer_url": trailer_url,
            "is_favorite": imdb_id in _favorite_ids(request.user),
        },
    )


@login_required
def add_favorite(request, imdb_id):
    if request.method == "POST":
        details = get_details(imdb_id)
        if details.get("Response") == "True":
            Favorite.objects.get_or_create(
                user=request.user,
                imdb_id=imdb_id,
                defaults={
                    "title": details.get("Title", ""),
                    "poster": details.get("Poster") if details.get("Poster") != "N/A" else "",
                    "year": details.get("Year", ""),
                },
            )
            messages.success(request, f'Added "{details.get("Title")}" to favorites.')
    next_url = request.POST.get("next") or "home"
    return redirect(next_url)


@login_required
def remove_favorite(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk, user=request.user)
    if request.method == "POST":
        favorite.delete()
    return redirect("favorites")


@login_required
def favorites(request):
    return render(request, "movies/favorites.html", {"favorites": request.user.favorites.all()})