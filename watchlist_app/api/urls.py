from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from watchlist_app.api.views import movie_list, movie_info
from watchlist_app.api.views import (MovieListAV, MovieInfoAV, StreamingPlatformVS, ReviewsCreate,
                                     ReviewsInfo, ReviewsList)

router = DefaultRouter()
router.register('platform', StreamingPlatformVS, basename='streamingplatform')
urlpatterns = router.urls

urlpatterns=[
    path('movies/', MovieListAV.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieInfoAV.as_view(), name='movie-detail'),
    path('', include(router.urls)),
    #path('platform/', StreamingPlatformListAV.as_view(), name='platform-list'),
    #path('platform/<int:pk>', StremingPlatformInfoAV.as_view(), name='streamingplatform-detail'),
    
    path('movie/<int:pk>/reviewscreate/', ReviewsCreate.as_view(), name='reviews-create'), 
    path('reviews/<int:pk>/', ReviewsInfo.as_view(), name='reviews-detail'),
    path('movie/<int:pk>/reviews/', ReviewsList.as_view(), name='reviews-list') 
]