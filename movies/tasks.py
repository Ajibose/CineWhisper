import logging
import requests
import json
from django.conf import settings
from django.core.cache import cache
from celery import shared_task
from django.db import transaction
from datetime import datetime
from .models import Movie, TvShow

logger = logging.getLogger(__name__)

def fetch_trending_data(url: str, total_pages: int) -> list:
    """Fetch trending data from TMDb"""
    all_results = []
    for page in range(1, total_pages + 1):
        params = {
            'api_key': settings.TMDB_API_KEY,
            'page': page
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            all_results.extend(data.get("results", []))
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {page} from {url}: {e}")
    return all_results

def parse_date(date_str):
    """Convert date string to a date object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def bulk_upsert_movies(movies: list):
    """Bulk upsert movie records and cache the results"""
    if not movies:
        return

    movie_ids = [movie["id"] for movie in movies]

    # Fetch existing movies by their TMDb id
    existing_movies = {m.tmdb_id: m for m in Movie.objects.filter(tmdb_id__in=movie_ids)}

    movies_to_create = []
    movies_to_update = []

    for movie in movies:
        parsed_data = {
            "tmdb_id": movie["id"],
            "backdrop_path": movie.get("backdrop_path", ""),
            "title": movie.get("title", ""),
            "original_title": movie.get("original_title", ""),
            "overview": movie.get("overview", ""),
            "poster_path": movie.get("poster_path", ""),
            "adult": movie.get("adult", False),
            "original_language": movie.get("original_language", ""),
            "genre_ids": json.dumps(movie.get("genre_ids", [])),  # Store as JSON string
            "popularity": movie.get("popularity", 0.0),
            "release_date": parse_date(movie.get("release_date")),
            "video": movie.get("video", False),
            "vote_average": movie.get("vote_average", 0.0),
            "vote_count": movie.get("vote_count", 0)
        }

        if parsed_data["tmdb_id"] in existing_movies:
            existing_movie = existing_movies[parsed_data["tmdb_id"]]
            for key, value in parsed_data.items():
                setattr(existing_movie, key, value)
            movies_to_update.append(existing_movie)
        else:
            movies_to_create.append(Movie(**parsed_data))

    with transaction.atomic():
        if movies_to_create:
            Movie.objects.bulk_create(movies_to_create, ignore_conflicts=True)  # ✅ Avoid duplicate errors

        if movies_to_update:
            Movie.objects.bulk_update(movies_to_update, [
                "backdrop_path", "title", "original_title", "overview", "poster_path",
                "adult", "original_language", "genre_ids", "popularity",
                "release_date", "video", "vote_average", "vote_count"
            ])

    cache.set("trending_movies", movies, timeout=7200)
    logger.info("Successfully fetched, cached, and stored trending movies.")

def bulk_upsert_tv_shows(tv_shows: list):
    """Bulk upsert TV show records and cache the results"""
    if not tv_shows:
        return

    tv_show_ids = [show["id"] for show in tv_shows]

    # Fetch existing TV shows by their TMDb ID
    existing_tv_shows = {s.tmdb_id: s for s in TvShow.objects.filter(tmdb_id__in=tv_show_ids)}

    tv_shows_to_create = []
    tv_shows_to_update = []

    for show in tv_shows:
        parsed_data = {
            "tmdb_id": show["id"],
            "backdrop_path": show.get("backdrop_path", ""),
            "name": show.get("name", ""),
            "original_name": show.get("original_name", ""),
            "overview": show.get("overview", ""),
            "poster_path": show.get("poster_path", ""),
            "adult": show.get("adult", False),
            "original_language": show.get("original_language", ""),
            "genre_ids": json.dumps(show.get("genre_ids", [])),  # ✅ Store as JSON
            "popularity": show.get("popularity", 0.0),
            "first_air_date": parse_date(show.get("first_air_date")),
            "vote_average": show.get("vote_average", 0.0),
            "vote_count": show.get("vote_count", 0),
            "origin_country": json.dumps(show.get("origin_country", []))  # ✅ Store as JSON
        }

        if parsed_data["tmdb_id"] in existing_tv_shows:
            existing_show = existing_tv_shows[parsed_data["tmdb_id"]]
            for key, value in parsed_data.items():
                setattr(existing_show, key, value)
            tv_shows_to_update.append(existing_show)
        else:
            tv_shows_to_create.append(TvShow(**parsed_data))

    with transaction.atomic():
        if tv_shows_to_create:
            TvShow.objects.bulk_create(tv_shows_to_create, ignore_conflicts=True)  # ✅ Avoid duplicate key errors

        if tv_shows_to_update:
            TvShow.objects.bulk_update(tv_shows_to_update, [
                "backdrop_path", "name", "original_name", "overview", "poster_path",
                "adult", "original_language", "genre_ids", "popularity",
                "first_air_date", "vote_average", "vote_count", "origin_country"
            ])

    cache.set("trending_tv_shows", tv_shows, timeout=7200)
    logger.info("Successfully fetched, cached, and stored trending TV shows.")

@shared_task
def fetch_trending_movies_shows():
    """Fetch, cache, and store trending movies and TV shows"""
    total_pages = 10
    movie_url = 'https://api.themoviedb.org/3/trending/movie/day'
    tv_url = 'https://api.themoviedb.org/3/trending/tv/day'
    
    movies = fetch_trending_data(movie_url, total_pages)
    tv_shows = fetch_trending_data(tv_url, total_pages)
    
    bulk_upsert_movies(movies)
    bulk_upsert_tv_shows(tv_shows)
    
    return "Fetched, cached, and stored trending movies and TV shows"

