from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid


class Movie(models.Model):
    """Model to store movies from tmdb"""
    tmdb_id = models.IntegerField(unique=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    adult = models.BooleanField(default=False)
    original_language = models.CharField(max_length=10, blank=True)
    genre_ids = ArrayField(models.IntegerField(), blank=True, default=list)
    popularity = models.FloatField(default=0.0)
    release_date = models.DateField(null=True, blank=True)
    video = models.BooleanField(default=False)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-popularity']

class TvShow(models.Model):
    """Model to store TV show from tmdb"""
    tmdb_id = models.IntegerField(unique=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255, blank=True)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    adult = models.BooleanField(default=False)
    original_language = models.CharField(max_length=10, blank=True)
    genre_ids = ArrayField(models.IntegerField(), blank=True, default=list)
    popularity = models.FloatField(default=0.0)
    first_air_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    origin_country = ArrayField(models.CharField(max_length=10), blank=True, default=list)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-popularity']

