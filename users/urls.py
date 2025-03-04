from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    MyTokenObtainPairView,
    RegisterView,
    UserViewSet,
    FavouriteViewSet,
)

router = DefaultRouter()

# Register viewsets for profile and favourites endpoints.
router.register(r'profile', UserViewSet, basename='profile')
router.register(r'favourites', FavouriteViewSet, basename='favourites')

urlpatterns = [
    # JWT authentication endpoints
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Registration endpoint
    path('auth/', RegisterView.as_view(), name='register'),
    
    # Include router URLs for profile and favourites
    path('', include(router.urls)),
]
