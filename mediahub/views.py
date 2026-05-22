from django.shortcuts import render
from django.http import HttpResponse



def home(request):
    top_movies = []#Media.objects.filter(media_type="movie").order_by("-average_rating")[:10]
    top_series = []#Media.objects.filter(media_type="series").order_by("-average_rating")[:10]
    top_anime = []#Media.objects.filter(media_type="anime").order_by("-average_rating")[:10]

    context = {
        "top_movies": top_movies,
        "top_series": top_series,
        "top_anime": top_anime,
    }

    return render(request, "mediahub/home.html", context)

def search(request):

    query = request.GET.get("query", "")

    results = []

    context = {
        "query": query,
        "results": results,
    }

    return render(request, "mediahub/search.html", context)
def movies_page(request):
    movies = []

    context = {
        "movies": movies
    }

    return render(request, "mediahub/movies.html", context)


def series_page(request):
    series = []

    context = {
        "series": series
    }

    return render(request, "mediahub/series.html", context)


def anime_page(request):
    anime = []

    context = {
        "anime": anime
    }

    return render(request, "mediahub/anime.html", context)