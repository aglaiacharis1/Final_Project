# movies/omdb.py
"""Thin wrapper around the OMDb API."""
import requests
from django.conf import settings

BASE_URL = "http://www.omdbapi.com/"
TIMEOUT = 8


def _get(params):
    params = {"apikey": settings.OMDB_API_KEY, **params}
    try:
        response = requests.get(BASE_URL, params=params, timeout=TIMEOUT)
        return response.json()
    except requests.RequestException:
        return {"Response": "False", "Error": "Could not reach OMDb right now."}


def search_movies(query, page=1):
    """Search by free-text title."""
    return _get({"s": query, "type": "movie", "page": page})


def search_by_genre_year(genre, year):
    """OMDb has no genre filter, so we search the genre as a keyword and
    narrow by year, same trick the original prototype used."""
    return _get({"s": genre, "type": "movie", "y": year})


def get_details(imdb_id):
    """Full details (plot, rating, cast, etc.) for one title."""
    return _get({"i": imdb_id, "plot": "full"})