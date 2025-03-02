import logging
import requests
from django.conf import settings
from django.core.cache import cache
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def fetch_trending_movies_shows():
    """Fetch and cache 10 pages of trending movies from TMDb"""
    movie_url = 'https://api.themoviedb.org/3/trending/movie/day'
    tv_url = 'https://api.themoviedb.org/3/trending/tv/day'

    all_movies = []  
    all_tv_shows = []

    total_pages = 10

    for page in range(1, total_pages + 1):
        params = {
            'api_key': settings.TMDB_API_KEY,
            'page': page
        }

        # Fetch trending movies
        try:
            movie_response = requests.get(movie_url, params=params, timeout=10)
            movie_response.raise_for_status()
            movie_data = movie_response.json()
            all_movies.extend(movie_data.get("results", []))  # Add movies from this page
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {page} of trending movies: {e}")

        # Fetch trending TV shows
        try:
            show_response = requests.get(tv_url, params=params, timeout=10)
            show_response.raise_for_status()
            show_data = show_response.json() 
            all_tv_shows.extend(show_data.get("results", []))
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {page} of trending TV shows: {e}")

    if all_movies:
        cache.set("trending_movies", all_movies, timeout=7200)  # Cache for 2 hours
        logger.info("Successfully fetched and cached 10 pages of trending movies")

    if all_tv_shows:
        cache.set("trending_tv_shows", all_tv_shows, timeout=7200)
        logger.info("Successfully fetched and cached 10 pages of trending TV shows")

    return "Fetched and cached trending movies and TV shows"

