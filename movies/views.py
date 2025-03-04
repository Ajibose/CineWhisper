from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.core.cache import cache
from .models import Movie
from .serializers import MovieSerializer, TvShowSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet to Movies
    Also includes custom endpoints for fetching trending movies and trending TV shows.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "movie_id"

    @action(detail=False, methods=['get'], url_path='trending')
    def trending_movies(self, request):
        """
        GET /movies/trending/movies - Fetch trending movies from cache.
        """
        trending_data = cache.get("trending_movies")

        if not trending_data:
            return Response({"error": "No trending movies"}, status=404)

	# Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = request.query_params.get('page_size', 10)
        page = paginator.paginate_queryset(trending_data, request)
        return paginator.get_paginated_response(page)



class TvShowViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet to TvShow
    Also includes custom endpoints for fetching trending movies and trending TV shows
    """
    queryset = Movie.objects.all()
    serializer_class = TvShowSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "show_id"

    @action(detail=False, methods=['get'], url_path='trending')
    def trending_tv_shows(self, request):
        """
        GET /movies/trending/tv_shows - Fetch trending TV shows from cache.
        """
        trending_data = cache.get("trending_tv_shows")

        if not trending_data:
            return Response({"error": "No trending TV shows"}, status=404)

        # Apply Pagination
        paginator = PageNumberPagination()
        paginator.page_size = request.query_params.get('page_size', 10)
        page = paginator.paginate_queryset(trending_data, request)

        return paginator.get_paginated_response(page) 
