from rest_framework import serializers
from watchlist_app.models import Movie, StreamingPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    editor = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude=('movies',)
        

class MovieSerializer(serializers.ModelSerializer):
    #reviews = ReviewSerializer(many=True, read_only=True)
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
    
    """def create(self, validated_data):
        movies_data=validated_data.pop('movies')
        platform = StreamingPlatform.objects.create(**validated_data)
        for movie_data in movies_data:
            Movie.objects.create(platform=platform, **movie_data)
        return platform """
        
    def get_movies(self, obj):
        return [movie.description for movie in obj.movies.all()]

    def validate(self, data):
        if data['name']==data['about']:
            raise serializers.ValidationError("Name must not be equal to description")
        return data
    

        
        
""" def name_length(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name must have more than 2 letters")
    elif len(value)>50:
        raise serializers.ValidationError("Name must have less than 50 letters")
    return value

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])
    description = serializers.CharField(max_length=500)
    active = serializers.BooleanField()
    ageRestriction = serializers.IntegerField()
    
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.ageRestriction = validated_data.get('ageRestriction', instance.ageRestriction)
        instance.save()
        return instance
    
    def validate(self, data):
        if data['name']==data['description']:
            raise serializers.ValidationError("Name must not be equal to description")
        return data
    
    
    def validate_ageRestriction(self, value):
        if value!=0 and value!=10 and value!=12 and value!=14 and value!=16 and value!=18:
            raise serializers.ValidationError("Age restriction not possible") 
        return value
     """
    
