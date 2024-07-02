from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from watchlist_app.models import Movie, StreamingPlatform
from  watchlist_app.api.serializers import MovieSerializer, StreamingPlatformSerializer

class StreamingPlatformListAV(APIView):

    def get(self, request):
        platforms=StreamingPlatform.objects.all()
        serializer=StreamingPlatformSerializer(platforms, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StremingPlatformInfoAV(APIView):
    
    def get(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return Response({'error': 'Streaming Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer= StreamingPlatformSerializer(platform, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        platform = StreamingPlatform.objects.get(pk=pk)
        serializer= StreamingPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    def delete(self, request, pk):
        platform=StreamingPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MovieListAV (APIView):
    
    def get(self, request):
        movies = Movie.objects.all()
        serializer= MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer= MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
       
class MovieInfoAV(APIView):
    
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