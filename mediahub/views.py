from django.shortcuts import render
from .services import (get_top_rated_movies,get_top_rated_series,get_top_rated_anime,get_top_by_category,get_media_details,search_media,get_search_genres)

BASE_URL = "https://image.tmdb.org/t/p/"
POSTER_SIZE = "w500"

def normalize_media_item(item, fallback_media_type=""):
    title = item.get("title") or item.get("name") or "Unknown title"
    release_date = item.get("release_date") or item.get("first_air_date") or ""
    poster_path = item.get("poster_path")

    poster_url = ""
    if poster_path:
        poster_url = f"{BASE_URL}{POSTER_SIZE}{poster_path}"

    return {
        "id": item.get("id"),
        "title": title,
        "media_type": item.get("media_type") or fallback_media_type,
        "rating": item.get("vote_average") or 0,
        "release_date": release_date,
        "description": item.get("overview") or "",
        "poster_url": poster_url,
        "genre_ids": item.get("genre_ids", []),
    }

def normalize_media_list(items, fallback_media_type=""):
    normalized_items = []

    for item in items:
        normalized_items.append(
            normalize_media_item(
                item,
                fallback_media_type=fallback_media_type,
            )
        )

    return normalized_items

def normalize_genre_sections(sections, fallback_media_type=""):
    normalized_sections = []

    for section in sections:
        genre_name = section.get("genre", "")
        items = section.get("items", [])

        normalized_sections.append({
            "genre": genre_name,
            "items": normalize_media_list(
                items,
                fallback_media_type=fallback_media_type,
            ),
        })

    return normalized_sections

def home(request):

    top_movies = normalize_media_list(
        get_top_rated_movies(),
        fallback_media_type="movie",
    )

    top_series = normalize_media_list(
        get_top_rated_series(),
        fallback_media_type="series",
    )

    top_anime = normalize_media_list(
        get_top_rated_anime(),
        fallback_media_type="anime",
    )

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

    genres = get_search_genres()
    results = []

    if has_search:
        results = normalize_media_list(search_media(query = query, genre_id = selected_genre))

    context = {
        "query": query,
        "selected_genre": selected_genre,
        "genres": genres,
        "results": results,
        "has_search": has_search,
    }

    return render(request, "mediahub/search.html", context)

def movies_page(request):

    genre_sections = normalize_genre_sections(
        get_top_by_category("movie"),
        fallback_media_type="movie",
    )

    context = {
        "genre_sections": genre_sections,
    }

    return render(request, "mediahub/movies.html", context)


def series_page(request):

    genre_sections = normalize_genre_sections(
        get_top_by_category("series"),
        fallback_media_type="series",
    )

    context = {
        "genre_sections": genre_sections,
    }

    return render(request, "mediahub/series.html", context)


def anime_page(request):

    genre_sections = normalize_genre_sections(
        get_top_by_category("anime"),
        fallback_media_type="anime",
    )

    context = {
        "genre_sections": genre_sections,
    }

    return render(request, "mediahub/anime.html", context)