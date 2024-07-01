from django.db import models

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