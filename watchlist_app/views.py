from django.shortcuts import render
from watchlist_app.models import Movie
from django.http import JsonResponse

def movie_list(request):
    movies = Movie.objects.all()
    data = {
        'movies': list(movies.values())
        }
    return JsonResponse(data)
    
def movie_info(request, pk):
    movie=Movie.objects.get(pk=pk)
    data = {
        'name': movie.name,
        'description': movie.description,
        'activated': movie.active,
        'agerestrict': movie.ageRestriction
    }
    return JsonResponse(data)