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

    def get_queryset(self):
        """
        Override to filter by TMDb ID if provided
        """
        queryset = Movie.objects.all()
        tmdb_id = self.request.query_params.get('tmdb_id')

        if tmdb_id:
            try:
                return queryset.filter(tmdb_id=int(tmdb_id))
            except ValueError:
                return Movie.objects.none()

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Custom list method to check TMDb API if not found in local DB
        """
        tmdb_id = self.request.query_params.get('tmdb_id')

        if tmdb_id:
            queryset = self.get_queryset()

            if queryset.exists():
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)

            # fetch from tmdb api if not in table
            tmdb_response = self.fetch_movie_from_tmdb(tmdb_id)
            if tmdb_response:
                return Response(tmdb_response, status=status.HTTP_200_OK)
            

            return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

        return super().list(request, *args, **kwargs)


    def fetch_movie_from_tmdb(tmdb_id):
        """
        Fetch movie from tmdb API
        """
        TMDB_API_KEY = settings.TMDB_API_KEY
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"

        movie_response = requests.get(url)
        if movie_response.status_code == 200:
            genres_id = [movie_response["genres"]["id"] for movie in movie_response]
            parsed_data = {
                "tmdb_id": movie_response.get("id"),
                "backdrop_path": movie_response.get("backdrop_path", ""),
                "title": movie_response.get("title", ""),
                "original_title": movie_response.get("original_title", ""),
                "overview": movie_response.get("overview", ""),
                "poster_path": movie_response.get("poster_path", ""),
                "adult": movie_response.get("adult", False),
                "original_language": movie_response.get("original_language", ""),
                "genre_ids": genres_id,
                "popularity": movie_response.get("popularity", 0.0),
                "release_date": parse_date(movie_response.get("release_date")),
                "video": movie_response.get("video", False),
                "vote_average": movie_response.get("vote_average", 0.0),
                "vote_count": movie_response.get("vote_count", 0)
            } 
            return parsed_data.json()

        return None


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
