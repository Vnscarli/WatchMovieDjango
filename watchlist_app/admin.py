from django.contrib import admin
from watchlist_app.models import Movie, StreamingPlatform, Review

admin.site.register(Movie)
admin.site.register(StreamingPlatform)
admin.site.register(Review)
