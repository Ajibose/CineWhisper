from django.db import models

class Movies(models.Model):
    movie_id = models.IntegerField(primary_key=True)
