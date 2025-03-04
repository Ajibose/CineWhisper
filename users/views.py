from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import (
        RegisterSerializer, MyTokenObtainPairSerializer,
        ProfileSerializer, FavouriteSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Favourite
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import AnonymousUser


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for retrieving and updating the authenticated user's profile
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'put', 'patch', 'delete']
    lookup_field = "user_id"

    def get_queryset(self):
        user = getattr(self.request, 'user', None)
        if not hasattr(self, 'request') or not self.request.user.is_authenticated:
             return User.objects.none()

        return User.objects.filter(pk=user.pk)


class FavouriteViewSet(viewsets.ModelViewSet):
    """
    viewset for managing a user's favorite movies or TV shows.

    Features:
      - Only authenticated users can access these endpoints.
      - The queryset is filtered to the current authenticated user's favourites.
      - Make sures that on creation, the current user is automatically assigned
      - Duplicate entries are prevented
    """
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'favourite_id'

    def get_queryset(self):
        """Get only the favourites belonging to the authenticated user"""
        if not hasattr(self, 'request') or not self.request.user.is_authenticated:
            return Favourite.objects.none()

        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Assign the current user to the favourite"""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Overide to catch duplicate entry errors and return a friendly error"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except IntegrityError:
            raise ValidationError("This item is already in your favourites")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
