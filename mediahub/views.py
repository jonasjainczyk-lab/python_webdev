from django.shortcuts import render, redirect
from .services import (get_top_rated_movies,get_top_rated_series,get_top_rated_anime,get_top_by_category,get_media_details,search_media,get_search_genres)
from django.db.models import Avg
from .forms import UserRatingForm
from .models import UserRating

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


def get_display_media_type(details, media_type):
    if media_type == "movie":
        return "movie"

    genres = details.get("genres", [])
    genre_names = [genre.get("name", "").lower() for genre in genres]

    origin_countries = details.get("origin_country", [])
    original_language = details.get("original_language", "")

    is_animation = "animation" in genre_names
    is_japanese = "JP" in origin_countries or original_language == "ja"

    if media_type == "tv" and is_animation and is_japanese:
        return "anime"

    return "series"


def home(request):

    top_movies = normalize_media_list(
        get_top_rated_movies(),
        fallback_media_type="movie",
    )

    top_series = normalize_media_list(
        get_top_rated_series(),
        fallback_media_type="tv",
    )

    top_anime = normalize_media_list(
        get_top_rated_anime(),
        fallback_media_type="tv",
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
        fallback_media_type="tv",
    )

    context = {
        "genre_sections": genre_sections,
    }

    return render(request, "mediahub/series.html", context)


def anime_page(request):

    genre_sections = normalize_genre_sections(
        get_top_by_category("anime"),
        fallback_media_type="tv",
    )

    context = {
        "genre_sections": genre_sections,
    }

    return render(request, "mediahub/anime.html", context)


def detail_page(request, media_type, media_id):
    details = get_media_details(
        media_id=media_id,
        media_type=media_type,
    )

    #display_media_type = ""

    #if details:
    #    display_media_type = get_display_media_type(details, media_type)

    user_rating = None

    if request.user.is_authenticated:
        user_rating = UserRating.objects.filter(
            user=request.user,
            media_id=media_id,
            media_type=media_type,
        ).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = UserRatingForm(request.POST, instance=user_rating)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.media_id = media_id
            rating.media_type = media_type
            rating.save()

            return redirect("detail", media_type=media_type, media_id=media_id)
    else:
        form = UserRatingForm(instance=user_rating)

    ratings = UserRating.objects.filter(
        media_id=media_id,
        media_type=media_type,
    ).select_related("user").order_by("-created_at")

    average_user_rating = ratings.aggregate(
        Avg("rating")
    )["rating__avg"]

    context = {
        "details": details,
        #"display_media_type": display_media_type,
        "media_type": media_type,
        "media_id": media_id,
        "form": form,
        "ratings": ratings,
        "average_user_rating": average_user_rating,
        "user_rating": user_rating,
        "not_found": details is None,
    }

    return render(request, "mediahub/detail.html", context)