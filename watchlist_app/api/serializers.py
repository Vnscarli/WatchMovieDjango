from rest_framework import serializers
from watchlist_app.models import Movie

def name_length(value):
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
    
    
