from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("movies/", views.movies_page, name="movies"),
    path("series/", views.series_page, name="series"),
    path("anime/", views.anime_page, name="anime"),
]