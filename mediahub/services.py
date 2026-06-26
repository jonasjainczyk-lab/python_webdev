import requests

# Key + base URL (Url unterteilt in den Teil der immer dransteht + spezifisches ende für jede API)
API_KEY = "2ddaaabb21abd7de40f977b45bc6ba61"
BASE_URL = "https://api.themoviedb.org/3"

# Schwellenwert um nur relevante Ergebnisse zu bekommen
MIN_VOTES = 500

# Für die Genre-basierte Suche die richtige genre-id finden für jeweils "movie" und "tv" Suche
SEARCH_GENRE_MAPPING = {
    "action": {
    "name": "Action",
    "movie_id": 28,
    "tv_id": 10759,
},
"adventure": {
    "name": "Abenteuer",
    "movie_id": 12,
    "tv_id": 10759,
},
    "animation": {
        "name": "Animation",
        "movie_id": 16,
        "tv_id": 16,
    },
    "comedy": {
        "name": "Komödie",
        "movie_id": 35,
        "tv_id": 35,
    },
    "crime": {
        "name": "Krimi",
        "movie_id": 80,
        "tv_id": 80,
    },
    "documentary": {
        "name": "Dokumentarfilm",
        "movie_id": 99,
        "tv_id": 99,
    },
    "drama": {
        "name": "Drama",
        "movie_id": 18,
        "tv_id": 18,
    },
    "family": {
        "name": "Familie",
        "movie_id": 10751,
        "tv_id": 10751,
    },
    "mystery": {
        "name": "Mystery",
        "movie_id": 9648,
        "tv_id": 9648,
    },
    "scifi_fantasy": {
        "name": "Sci-Fi & Fantasy",
        "movie_id": 878,
        "tv_id": 10765,
    },
    "western": {
        "name": "Western",
        "movie_id": 37,
        "tv_id": 37,
    },

    # Nur Movie vorhanden
    "history": {
        "name": "Historie",
        "movie_id": 36,
        "tv_id": None,
    },
    "horror": {
        "name": "Horror",
        "movie_id": 27,
        "tv_id": None,
    },
    "music": {
        "name": "Musik",
        "movie_id": 10402,
        "tv_id": None,
    },
    "romance": {
        "name": "Liebesfilm",
        "movie_id": 10749,
        "tv_id": None,
    },
    "tv_movie": {
        "name": "TV-Film",
        "movie_id": 10770,
        "tv_id": None,
    },
    "thriller": {
        "name": "Thr+iller",
        "movie_id": 53,
        "tv_id": None,
    },
    "war_movie": {
        "name": "Kriegsfilm",
        "movie_id": 10752,
        "tv_id": None,
    },

    # Nur TV vorhanden
    "kids": {
        "name": "Kids",
        "movie_id": None,
        "tv_id": 10762,
    },
    "news": {
        "name": "News",
        "movie_id": None,
        "tv_id": 10763,
    },
    "reality": {
        "name": "Reality",
        "movie_id": None,
        "tv_id": 10764,
    },
    "soap": {
        "name": "Soap",
        "movie_id": None,
        "tv_id": 10766,
    },
    "talk": {
        "name": "Talk",
        "movie_id": None,
        "tv_id": 10767,
    },
    "war_politics": {
        "name": "War & Politics",
        "movie_id": None,
        "tv_id": 10768,
    },
}

def get_search_genres():
    genres = []

    for genre_key, genre_data in SEARCH_GENRE_MAPPING.items():
        genres.append({
            "id": genre_key,
            "name": genre_data["name"],
        })

    return genres

# APIs für Top Rated (jeweils 10)


# def get_top_rated_movies():
#     """Holt die 10 am besten bewerteten Filme aller Zeiten"""
#     url = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&language=de-DE"
#     response = requests.get(url)
#     return response.json().get("results", [])[:30] if response.status_code == 200 else []

def get_top_rated_movies(limit=10):
    """Holt die am besten bewerteten Filme."""
    results = []
    page = 1

    while len(results) < limit:
        url = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&language=de-DE&page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            break

        page_results = response.json().get("results", [])

        if not page_results:
            break

        results.extend(page_results)
        page += 1

    return results[:limit]


# def get_top_rated_series():
#     """Holt die 10 am besten bewerteten Serien aller Zeiten"""
#     url = f"{BASE_URL}/tv/top_rated?api_key={API_KEY}&language=de-DE"
#     response = requests.get(url)
#     return response.json().get("results", [])[:30] if response.status_code == 200 else []

def get_top_rated_series(limit=10):
    """Holt die am besten bewerteten Serien."""
    results = []
    page = 1

    while len(results) < limit:
        url = f"{BASE_URL}/tv/top_rated?api_key={API_KEY}&language=de-DE&page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            break

        page_results = response.json().get("results", [])

        if not page_results:
            break

        results.extend(page_results)
        page += 1

    return results[:limit]

# def get_top_rated_anime():
#     """Holt die 10 am besten bewerteten Anime"""
#     url = (f"{BASE_URL}/discover/tv?api_key={API_KEY}&language=de-DE"
#            f"&with_genres=16&with_original_language=ja"
#            f"&sort_by=vote_average.desc&vote_count.gte={MIN_VOTES}")
#     response = requests.get(url)
#     return response.json().get("results", [])[:10] if response.status_code == 200 else []

def get_top_rated_anime(limit=10):
    """Holt die am besten bewerteten japanischen Anime."""
    results = []
    page = 1

    while len(results) < limit:
        url = (
            f"{BASE_URL}/discover/tv?api_key={API_KEY}&language=de-DE"
            f"&with_genres=16&with_original_language=ja"
            f"&sort_by=vote_average.desc&vote_count.gte={MIN_VOTES}"
            f"&page={page}"
        )

        response = requests.get(url)

        if response.status_code != 200:
            break

        page_results = response.json().get("results", [])

        if not page_results:
            break

        results.extend(page_results)
        page += 1

    return results[:limit]

# API für Top Rated Pro Kategorie

def get_top_by_category(media_type):
    if media_type == "movie":
        categories = [
            {"id": 28, "name": "Top Actionfilme"},
            {"id": 35, "name": "Top Komödien"},
            {"id": 878, "name": "Top Sci-Fi"},
            {"id": 10749, "name": "Top Romantik"},
            {"id": 53, "name": "Top Thriller"},
            {"id": 18, "name": "Top Drama"},
            {"id": 27, "name": "Top Horror"}
        ]
    elif media_type == "series":
        categories = [
            {"id": 10759, "name": "Top Action & Adventure"},
            {"id": 18, "name": "Top Dramen"},
            {"id": 9648, "name": "Top Mystery"},
            {"id": 80, "name": "Top Krimi"},
            {"id": 10762, "name": "Top Kids-Show"}
        ]
    elif media_type == "anime":
        categories = [
            {"id": 10759, "name": "Top Action Anime"},
            {"id": 10765, "name": "Top Sci-Fi & Fantasy Anime"},
            {"id": 35, "name": "Top Comedy Anime"},
            {"id": 10766, "name": "Top Romance/Slice of Life Anime"}
        ]
    else:
        return []

    sections = []
    for cat in categories:
        if media_type == "anime":
            url = (f"{BASE_URL}/discover/tv?api_key={API_KEY}&language=de-DE"
                   f"&with_original_language=ja&with_genres=16,{cat['id']}"
                   f"&sort_by=vote_average.desc&vote_count.gte={MIN_VOTES}")
        elif media_type == "series":
            url = (f"{BASE_URL}/discover/tv?api_key={API_KEY}&language=de-DE"
                   f"&with_genres={cat['id']}"
                   f"&sort_by=vote_average.desc&vote_count.gte={MIN_VOTES}")
        else:
            url = (f"{BASE_URL}/discover/movie?api_key={API_KEY}&language=de-DE"
                   f"&with_genres={cat['id']}"
                   f"&sort_by=vote_average.desc&vote_count.gte={MIN_VOTES}")

        response = requests.get(url)
        if response.status_code == 200:
            item_limit = 10

            if media_type in ["movie", "series"]:
                item_limit = 30

            sections.append({
                "genre": cat["name"],
                "items": response.json().get("results", [])[:item_limit]
            })

    return sections


# API für globale Suche

def global_search(query):
    """
    Sucht unscharf nach dem Begriff über ALLES hinweg (Filme, Serien, Anime).
    """
    if not query:
        return []

    url = f"{BASE_URL}/search/multi?api_key={API_KEY}&query={query}&language=de-DE"
    response = requests.get(url)

    if response.status_code == 200:
        results = response.json().get("results", [])
        media_results = [item for item in results if item.get("media_type") in ["movie", "tv"]]
        return media_results

    return []

# API für Genre Suche
def search_by_genre(genre_id):
    genre_data = SEARCH_GENRE_MAPPING.get(genre_id)

    if not genre_data:
        return []

    results = []

    movie_genre_id = genre_data.get("movie_id")
    tv_genre_id = genre_data.get("tv_id")

    if movie_genre_id:
        movie_url = (
            f"{BASE_URL}/discover/movie?api_key={API_KEY}&language=de-DE"
            f"&with_genres={movie_genre_id}"
            f"&sort_by=vote_average.desc&vote_count.gte={MIN_VOTES}"
        )

        movie_response = requests.get(movie_url)

        if movie_response.status_code == 200:
            movie_results = movie_response.json().get("results", [])

            for item in movie_results:
                item["media_type"] = "movie"

            results.extend(movie_results)

    if tv_genre_id:
        tv_url = (
            f"{BASE_URL}/discover/tv?api_key={API_KEY}&language=de-DE"
            f"&with_genres={tv_genre_id}"
            f"&sort_by=vote_average.desc&vote_count.gte={MIN_VOTES}"
        )

        tv_response = requests.get(tv_url)

        if tv_response.status_code == 200:
            tv_results = tv_response.json().get("results", [])

            for item in tv_results:
                item["media_type"] = "tv"

            results.extend(tv_results)

    results.sort(key=lambda item: item.get("vote_average", 0), reverse=True)

    return results

# Kombinierte Global + Genre Suche
def search_media(query="", genre_id=""):
    if query:
        results = global_search(query)
    elif genre_id:
        results = search_by_genre(genre_id)
    else:
        results = []

    if query and genre_id:
        genre_data = SEARCH_GENRE_MAPPING.get(genre_id)

        if not genre_data:
            return results

        movie_genre_id = genre_data.get("movie_id")
        tv_genre_id = genre_data.get("tv_id")

        filtered_results = []

        for item in results:
            item_media_type = item.get("media_type")
            item_genre_ids = item.get("genre_ids", [])

            if item_media_type == "movie" and movie_genre_id is not None and movie_genre_id in item_genre_ids:
                filtered_results.append(item)

            elif item_media_type == "tv" and tv_genre_id is not None and tv_genre_id in item_genre_ids:
                filtered_results.append(item)

        results = filtered_results

    return results

# API für Deatillansicht

def get_media_details(media_id, media_type="movie"):
    """
    Holt alle Details zu einem Film oder einer Serie anhand der ID.
    media_type muss entweder "movie" (für Filme) oder "tv" (für Serien/Anime) sein.
    """
    url = (f"{BASE_URL}/{media_type}/{media_id}?api_key={API_KEY}&language=de-DE"
           f"&append_to_response=credits,videos,watch/providers")

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    return None

"""Funktion um Review im UserRating model zu speichern"""

from .models import UserRating


def save_user_review(user, media_id, media_type, media_title, poster_path, rating, text):

    review, created = UserRating.objects.update_or_create(
        user=user,
        media_id=media_id,
        media_type=media_type,
        defaults={
            'media_title': media_title,
            'poster_path': poster_path,
            'rating': rating,
            'text': text
        }
    )
    return review