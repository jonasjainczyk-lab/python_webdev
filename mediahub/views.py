from django.shortcuts import render
from django.db.models import Q
#from .models import Media

def home(request):
    top_movies = []#Media.objects.filter(media_type="movie").order_by("-rating")[:20]
    top_series = []#Media.objects.filter(media_type="series").order_by("-rating")[:20]
    top_anime = []#Media.objects.filter(media_type="anime").order_by("-rating")[:20]

    context = {
        "top_movies": top_movies,
        "top_series": top_series,
        "top_anime": top_anime,
    }

    return render(request, "mediahub/home.html", context)

def search(request):

    query = request.GET.get("query", "").strip()
    selected_genre = request.GET.get("genre", "").strip()
    has_search = bool(query or selected_genre)

    genres = []
    results = []

    # Später mit Datenbank:
    #
    # genres = Media.objects.values_list("genre", flat=True).distinct().order_by("genre")
    # if has_search:
    #     results = Media.objects.all()
    #
    #     if query:
    #         results = results.filter(
    #             Q(title__icontains=query) |
    #             Q(actors__icontains=query) |
    #             Q(director__icontains=query)
    #         ).distinct()
    #
    #     if selected_genre:
    #         results = results.filter(genre=selected_genre)

    context = {
        "query": query,
        "selected_genre": selected_genre,
        "genres": genres,
        "results": results,
        "has_search": has_search,
    }

    return render(request, "mediahub/search.html", context)
def movies_page(request):
    genre_sections = []

    # Später mit Datenbank:
    #
    # genres = Media.objects.filter(
    #     media_type="movie"
    # ).values_list("genre", flat=True).distinct().order_by("genre")
    #
    # for genre in genres:
    #     movies = Media.objects.filter(
    #         media_type="movie",
    #         genre=genre
    #     ).order_by("-rating")
    #
    #     genre_sections.append({
    #         "genre": genre,
    #         "items": movies,
    #     })

    context = {
        "genre_sections": genre_sections,           # list with genres and their movies 
    }

    return render(request, "mediahub/movies.html", context)


def series_page(request):
    genre_sections = []

    # Später mit Datenbank:
    #
    # genres = Media.objects.filter(
    #     media_type="series"
    # ).values_list("genre", flat=True).distinct().order_by("genre")
    #
    # for genre in genres:
    #     series = Media.objects.filter(
    #         media_type="series",
    #         genre=genre
    #     ).order_by("-rating")
    #
    #     genre_sections.append({
    #         "genre": genre,
    #         "items": series,
    #     })

    context = {
        "genre_sections": genre_sections,
    }

    return render(request, "mediahub/series.html", context)


def anime_page(request):
    genre_sections = []

    # Später mit Datenbank:
    #
    # genres = Media.objects.filter(
    #     media_type="anime"
    # ).values_list("genre", flat=True).distinct().order_by("genre")
    #
    # for genre in genres:
    #     anime = Media.objects.filter(
    #         media_type="anime",
    #         genre=genre
    #     ).order_by("-rating")
    #
    #     genre_sections.append({
    #         "genre": genre,
    #         "items": anime,
    #     })

    context = {
        "genre_sections": genre_sections,
    }

    return render(request, "mediahub/anime.html", context)