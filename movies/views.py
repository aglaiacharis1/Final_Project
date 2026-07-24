# movies/views.py
from django.views.generic import TemplateView

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'movies/home.html'

class AboutPageView(TemplateView):
    template_name = 'movies/about.html'
