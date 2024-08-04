from rest_framework import serializers
from watchlist_app.models import Movie, StreamingPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    editor = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude=('movies',)
        

class MovieSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='platform.name')
    len_description = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields="__all__"
       
    def get_len_description(self, object):
        return len(object.description)
    
    def validate(self, data):
        if data['name']==data['description']:
            raise serializers.ValidationError("Name must not be equal to description")
        return data
    
    
    def validate_ageRestriction(self, value):
        if value!=0 and value!=10 and value!=12 and value!=14 and value!=16 and value!=18:
            raise serializers.ValidationError("Age restriction not possible") 
        return value
    
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name must have more than 2 letters")
        if len(value) > 50:
            raise serializers.ValidationError("Name must have less than 50 letters")
        return value

class StreamingPlatformSerializer(serializers.HyperlinkedModelSerializer):
    movies = serializers.SerializerMethodField()
    class Meta:
        model = StreamingPlatform
        exclude =[]
        
    def get_movies(self, obj):
        return [movie.description for movie in obj.movies.all()]

    def validate(self, data):
        if data['name']==data['about']:
            raise serializers.ValidationError("Name must not be equal to description")
        return data
