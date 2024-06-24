from django.urls import path
#from watchlist_app.api.views import movie_list, movie_info
from watchlist_app.api.views import MovieListAV, MovieInfoAV

urlpatterns=[
    path('list/', MovieListAV.as_view(), name='movie-list'),
    path('<int:pk>/', MovieInfoAV.as_view(), name='movie-info')
]