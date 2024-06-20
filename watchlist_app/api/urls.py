from django.urls import path
from watchlist_app.api.views import movie_list, movie_info

urlpatterns=[
    path('list/', movie_list, name='movie-list'),
    path('<int:pk>/', movie_info, name='movie-info')
]