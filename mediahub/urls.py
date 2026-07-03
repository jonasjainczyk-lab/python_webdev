from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("search/", views.search, name="search"),
    path("movies/", views.movies_page, name="movies"),
    path("series/", views.series_page, name="series"),
    path("anime/", views.anime_page, name="anime"),
    path("details/<str:media_type>/<int:media_id>/", views.detail_page, name="detail"),
    path("auth/", include("users.urls")),
    path("profile/", views.user_profile, name="user_profile"),
]