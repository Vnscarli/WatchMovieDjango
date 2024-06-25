from django.db import models

# Create your models here.
class Movie(models.Model):
    name = models.CharField()
    description = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    ageRestriction = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name