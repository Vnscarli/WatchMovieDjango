from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from django.shortcuts import get_object_or_404
import django_filters.rest_framework
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins, generics
from rest_framework import  filters
from watchlist_app.models import Movie, StreamingPlatform, Review
from watchlist_app.api.serializers import MovieSerializer, StreamingPlatformSerializer, ReviewSerializer
from watchlist_app.api.permissions import IsAdminorReadOnly, IsReviewOwnerorReadOnly
from watchlist_app.api.throttling import RevieewListThrottle, ReviewCreateThrottle
from watchlist_app.api.filters import MovieFilter

class UserReviews(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        #username = self.kwargs['username']
        username= self.request.query_params.get('username', None)
        return Review.objects.filter(editor__username=username)
    

class ReviewsCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = Movie.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset= Review.objects.filter(movies=movie, editor=review_user)
        
        if review_queryset.exists():
            raise ValidationError("Let others review this movie!!")
        
        serializer.save(movies=movie, editor=review_user)

class ReviewsList(generics.ListAPIView):
    serializer_class=ReviewSerializer
    throttle_classes = [RevieewListThrottle]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['editor__username', 'rating']
    
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(movies=pk)
    
class ReviewsInfo(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsReviewOwnerorReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    
    
    
class StreamingPlatformVS(viewsets.ModelViewSet): #You can use read only to avoid changing database
    permission_classes=[IsAdminorReadOnly]
    queryset=StreamingPlatform.objects.all()
    serializer_class=StreamingPlatformSerializer
    
    
    
""" Example of viewset  
   def list(self, request):
        queryset=StreamingPlatform.objects.all()
        serializer=StreamingPlatformSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset=StreamingPlatform.objects.all()
        platform = get_object_or_404(queryset, pk=pk)
        serializer=StreamingPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)
    """
        
    
""" Using mixins to list all the platforms
class StreamingPlatformListAV(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              generics.GenericAPIView):
    queryset= StreamingPlatform.objects.all()
    serializer_class= StreamingPlatformSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs) """
    
    
""" def get(self, request):
        platforms=StreamingPlatform.objects.all()
        serializer=StreamingPlatformSerializer(platforms, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """
    
""" Using mixins to get specific platform 
class StremingPlatformInfoAV(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics. GenericAPIView):
    queryset= StreamingPlatform.objects.all()
    serializer_class= StreamingPlatformSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) """

class MovieListAV (APIView):
    permission_classes=[IsAdminorReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = MovieFilter
    
    def get(self, request):
        queryset = Movie.objects.all()
        filtered_queryset = self.filterset_class(request.GET, queryset=queryset).qs
        serializer= MovieSerializer(filtered_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer= MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
       
class MovieInfoAV(APIView):
    permission_classes=[IsAdminorReadOnly]
    
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    
    
""" @api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer= MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer= MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'PUT', 'DELETE'])
def movie_info(request, pk):/
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) """