from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings
import requests
#from .models import FavoriteMovie

class MovieViewSet(viewsets.ViewSet):
    """Handles fetching trending movies and retrieving a single movie"""

    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'], url_path='trending/mvoies')
    def trending_movies(self, request):
        """ GET /movies/trending/ - Fetch trending movies """
        movies = cache.get("trending_movies")
        if not movies:
            return Response({"error": "No trending movies"}, status=404)

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = request.query_params.get('page_size', 10)
        page = paginator.paginate_queryset(movies, request)

        return paginator.get_paginated_response(page)

    @action(detail=False, methods=['get'], url_path='trending/tv_shows')
    def trending_tv_shows(self, request):
        """ GET /movies/trending/ - Fetch trending tv shows"""
        shows = cache.get("trending_tv_shows") 
        if not shows:
            return Response({"error": "No trending TV shows"}, status=404)

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = request.query_params.get('page_size', 10)
        page = paginator.paginate_queryset(shows, request)

        return paginator.get_paginated_response(page)
