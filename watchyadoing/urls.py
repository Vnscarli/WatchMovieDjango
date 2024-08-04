from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('watchlist/', include('watchlist_app.api.urls')),
    path('user/', include('user_app.api.urls')),
]
