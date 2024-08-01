import django_filters
from watchlist_app.models import Movie

class MovieFilter(django_filters.FilterSet):
    class Meta:
        model = Movie
        fields = {
            'name': ['exact', 'icontains'],  # Filter by exact match or partial match (case-insensitive)
            'genre': ['exact', 'icontains'],  # Filter by exact match or partial match (case-insensitive)
        }
