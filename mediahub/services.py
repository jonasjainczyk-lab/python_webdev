import requests

# Key + base URL (Url unterteilt in den Teil der immer dransteht + spezifisches ende für jede API)
API_KEY = "2ddaaabb21abd7de40f977b45bc6ba61"
BASE_URL = "https://api.themoviedb.org/3"

# Schwellenwert um nur relevante Ergebnisse zu bekommen
MIN_VOTES = 500



# APIs für Top Rated (jeweils 10)

def get_top_rated_movies():
    """Holt die 10 am besten bewerteten Filme aller Zeiten"""
    url = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&language=de-DE"
    response = requests.get(url)
    return response.json().get("results", [])[:10] if response.status_code == 200 else []


def get_top_rated_series():
    """Holt die 10 am besten bewerteten Serien aller Zeiten"""
    url = f"{BASE_URL}/tv/top_rated?api_key={API_KEY}&language=de-DE"
    response = requests.get(url)
    return response.json().get("results", [])[:10] if response.status_code == 200 else []


def get_top_rated_anime():
    """Holt die 10 am besten bewerteten Anime"""
    url = (f"{BASE_URL}/discover/tv?api_key={API_KEY}&language=de-DE"
           f"&with_genres=16&with_original_language=ja"
           f"&sort_by=vote_average.desc&vote_count.gte={MIN_VOTES}")
    response = requests.get(url)
    return response.json().get("results", [])[:10] if response.status_code == 200 else []



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
            sections.append({
                "genre": cat["name"],
                "items": response.json().get("results", [])[:10]  # Jeweils die Top 10 abschneiden
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