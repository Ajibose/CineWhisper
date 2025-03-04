from rest_framework import serializers
from .models import Movie, TvShow

class MovieSerializer(serializers.ModelSerializer):
    media_type = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__' 

    def get_media_type(self, obj):
        return "movie"


class TvShowSerializer(serializers.ModelSerializer):
    media_type = serializers.SerializerMethodField()

    class Meta:
        model = TvShow
        fields = '__all__' 

    def get_media_type(self, obj):
        return "tv"
