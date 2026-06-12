from django.shortcuts import render, redirect
from .services import (get_top_rated_movies,get_top_rated_series,get_top_rated_anime,get_top_by_category,get_media_details,search_media,get_search_genres, save_user_review)
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


def normalize_detail(details, media_type):
    if not details:
        return None

    is_movie = media_type == "movie"
    is_tv = media_type == "tv"

    if is_movie:
        title = details.get("title") or "Unknown title"
        release_date = details.get("release_date") or ""
        runtime = details.get("runtime")
        number_of_seasons = None
        number_of_episodes = None
        episode_run_time = []
    elif is_tv:
        title = details.get("name") or "Unknown title"
        release_date = details.get("first_air_date") or ""
        runtime = None
        number_of_seasons = details.get("number_of_seasons")
        number_of_episodes = details.get("number_of_episodes")
        episode_run_time = details.get("episode_run_time", [])
    else:
        title = details.get("title") or details.get("name") or "Unknown title"
        release_date = details.get("release_date") or details.get("first_air_date") or ""
        runtime = details.get("runtime")
        number_of_seasons = details.get("number_of_seasons")
        number_of_episodes = details.get("number_of_episodes")
        episode_run_time = details.get("episode_run_time", [])

    poster_path = details.get("poster_path") or ""

    poster_url = ""
    if poster_path:
        poster_url = f"{BASE_URL}{POSTER_SIZE}{poster_path}"

    credits = details.get("credits", {})
    cast = credits.get("cast", [])[:10]
    crew = credits.get("crew", [])

    directors = [
        person for person in crew
        if person.get("job") == "Director"
    ]

    return {
        "id": details.get("id"),
        "title": title,
        "media_type": media_type,
        "description": details.get("overview") or "",
        "release_date": release_date,
        "rating": details.get("vote_average") or 0,
        "poster_path": poster_path,
        "poster_url": poster_url,
        "genres": details.get("genres", []),

        "runtime": runtime,
        "episode_run_time": episode_run_time,
        "number_of_seasons": number_of_seasons,
        "number_of_episodes": number_of_episodes,

        "cast": cast,
        "directors": directors,
        "created_by": details.get("created_by", []),
    }



def get_display_media_type(details, media_type):
    if not details:
        return media_type

    genres = details.get("genres", [])
    genre_names = [
        genre.get("name", "").lower()
        for genre in genres
    ]

    origin_countries = details.get("origin_country", [])

    production_countries = details.get("production_countries", [])
    production_country_codes = [
        country.get("iso_3166_1")
        for country in production_countries
    ]

    spoken_languages = details.get("spoken_languages", [])
    spoken_language_codes = [
        language.get("iso_639_1")
        for language in spoken_languages
    ]
    spoken_language_names = [
        (language.get("english_name") or language.get("name") or "").lower()
        for language in spoken_languages
    ]

    is_animation = "animation" in genre_names

    is_japanese_origin = (
            "JP" in origin_countries
            or "JP" in production_country_codes
    )

    is_japanese_language = (
            "ja" in spoken_language_codes
            or "japanese" in spoken_language_names
            or "日本語" in spoken_language_names
    )

    if is_animation and is_japanese_origin and is_japanese_language:
        return "anime"

    if media_type == "movie":
        return "movie"

    if media_type == "tv":
        return "series"

    return media_type


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

    media = normalize_detail(details, media_type)

    display_media_type = ""

    if details:
        display_media_type = get_display_media_type(details, media_type)

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
            media_title = ""
            poster_path = ""

            if media:
                media_title = media["title"]
                poster_path = media["poster_path"]

            save_user_review(
                user=request.user,
                media_id=media_id,
                media_type=media_type,
                media_title=media_title,
                poster_path=poster_path,
                rating=form.cleaned_data["rating"],
                text=form.cleaned_data["text"],
            )

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
        "media" : media,
        "display_media_type": display_media_type,
        "media_type": media_type,
        "media_id": media_id,
        "form": form,
        "ratings": ratings,
        "average_user_rating": average_user_rating,
        "user_rating": user_rating,
        "not_found": details is None,
    }

    return render(request, "mediahub/details.html", context)