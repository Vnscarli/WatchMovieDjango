from django.shortcuts import get_object_or_404
import django_filters.rest_framework

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.pagination import LimitOffsetPagination

from rest_framework import viewsets, status, generics, filters

from watchlist_app import models
from watchlist_app.api import serializers, permissions, throttling, pagination
from watchlist_app.api.filters import MovieFilter

class UserReviews(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    
    def get_queryset(self):
        username= self.request.query_params.get('username', None)
        return models.Review.objects.filter(editor__username=username)
    

class ReviewsCreate(generics.CreateAPIView):
    serializer_class=serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]
    
    def get_queryset(self):
        return models.Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = models.Movie.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset= models.Review.objects.filter(movies=movie, editor=review_user)
        
        if review_queryset.exists():
            raise ValidationError("Let others review this movie!!")
        
        serializer.save(movies=movie, editor=review_user)

class ReviewsList(generics.ListAPIView):
    serializer_class=serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['editor__username', 'rating']
    pagination_class = pagination.ReviewsCPagination
    
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(movies=pk)
    
class ReviewsInfo(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Review.objects.all()
    serializer_class=serializers.ReviewSerializer
    permission_classes=[permissions.IsReviewOwnerorReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    
    
    
class StreamingPlatformVS(viewsets.ModelViewSet): #You can use read only to avoid changing database
    permission_classes=[permissions.IsAdminorReadOnly]
    queryset=models.StreamingPlatform.objects.all()
    serializer_class=serializers.StreamingPlatformSerializer
    

class MovieListAV (APIView):
    permission_classes=[permissions.IsAdminorReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = MovieFilter
    
    
    def get(self, request):
        queryset = models.Movie.objects.all()
        filtered_queryset = self.filterset_class(request.GET, queryset=queryset).qs
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(filtered_queryset, request)
        serializer= serializers.MovieSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer= serializers.MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
       
class MovieInfoAV(APIView):
    permission_classes=[permissions.IsAdminorReadOnly]
    
    def get(self, request, pk):
        try:
            movie = models.Movie.objects.get(pk=pk)
        except models.Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        movie = models.Movie.objects.get(pk=pk)
        serializer = serializers.MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        movie = models.Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
