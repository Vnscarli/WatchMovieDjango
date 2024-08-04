from django.urls import path, include
from rest_framework.routers import DefaultRouter

from watchlist_app.api import views 

router = DefaultRouter()
router.register('platform', views.StreamingPlatformVS, basename='streamingplatform')
urlpatterns = router.urls

urlpatterns=[
    path('movies/', views.MovieListAV.as_view(), name='movie-list'),
    path('movies/<int:pk>/', views.MovieInfoAV.as_view(), name='movie-detail'),
    path('', include(router.urls)),
    
    path('movie/<int:pk>/reviewscreate/', views.ReviewsCreate.as_view(), name='reviews-create'), 
    path('reviews/<int:pk>/', views.ReviewsInfo.as_view(), name='reviews-detail'),
    path('reviews/', views.UserReviews.as_view(), name='user-review-detail'),
    path('movie/<int:pk>/reviews/', views.ReviewsList.as_view(), name='reviews-list'),
    
]