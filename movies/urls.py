from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, TvShowViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movies')
router.register(r'tvshows', MovieViewSet, basename='tvshow')

urlpatterns = [
    path('', include(router.urls)),
]
