from django.urls import path
#from watchlist_app.api.views import movie_list, movie_info
from watchlist_app.api.views import (MovieListAV, MovieInfoAV, StreamingPlatformListAV, ReviewsCreate,
                                     StremingPlatformInfoAV, ReviewsInfo, ReviewsList)

urlpatterns=[
    path('movies/', MovieListAV.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieInfoAV.as_view(), name='movie-detail'),
    
    path('platform/', StreamingPlatformListAV.as_view(), name='platform-list'),
    path('platform/<int:pk>', StremingPlatformInfoAV.as_view(), name='streamingplatform-detail'),
    
    path('platform/<int:pk>/reviewscreate', ReviewsCreate.as_view(), name='reviews-create'),
    path('reviews/<int:pk>', ReviewsInfo.as_view(), name='reviews-detail'),
    path('platform/<int:pk>/reviews', ReviewsList.as_view(), name='reviews-list')
]