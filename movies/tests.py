from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Favorite, Movie

User = get_user_model()


class MoviePagesTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_about_page_loads(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_catalog_page_loads(self):
        response = self.client.get(reverse("catalog"))
        self.assertEqual(response.status_code, 200)

    def test_favorites_requires_login(self):
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 302)

    def test_favorites_accessible_when_logged_in(self):
        User.objects.create_user(username="tester", password="testpass123")
        self.client.login(username="tester", password="testpass123")
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 200)


class MovieModelTests(TestCase):
    def test_movie_str_returns_title(self):
        movie = Movie.objects.create(
            title="Inception", description="A dream heist.", release_year=2010
        )
        self.assertEqual(str(movie), "Inception")


class FavoriteModelTests(TestCase):
    def test_favorite_str_includes_user(self):
        user = User.objects.create_user(username="tester", password="testpass123")
        fav = Favorite.objects.create(
            user=user, imdb_id="tt1375666", title="Inception", year="2010"
        )
        self.assertIn("Inception", str(fav))
        self.assertIn("tester", str(fav))

    def test_duplicate_favorite_not_allowed(self):
        user = User.objects.create_user(username="tester", password="testpass123")
        Favorite.objects.create(user=user, imdb_id="tt1375666", title="Inception")
        with self.assertRaises(Exception):
            Favorite.objects.create(user=user, imdb_id="tt1375666", title="Inception")