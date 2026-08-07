# movies/omdb.py

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
    return _get({"s": query, "type": "movie", "page": page})


def search_by_genre_year(genre, year):
 
    return _get({"s": genre, "type": "movie", "y": year})


def get_details(imdb_id):
    return _get({"i": imdb_id, "plot": "full"})