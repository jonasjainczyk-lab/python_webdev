from django.shortcuts import render
from django.http import HttpResponse



def home(request):
    return render(request, "mediahub/home.html")


def movies_page(request):
    return render(request, "mediahub/movies.html")


def series_page(request):
    return render(request, "mediahub/series.html")


def anime_page(request):
    return render(request, "mediahub/anime.html")