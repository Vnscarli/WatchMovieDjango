from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class StreamingPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField()
    description = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    ageRestriction = models.IntegerField(default=0)
    genre = models.CharField(default="Escolher")
    platform = models.ForeignKey(StreamingPlatform, on_delete=models.SET_NULL, null=True, blank=True, related_name="movies")
    
    def __str__(self):
        return self.name

    
class Review(models.Model):
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),  MaxValueValidator(10)])
    movies = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + " " + self.movies.name
    