#manage the imports 
from rest_framework import serializers
from voting.models import Position
from voting.models import Election


class PositionSerializer(serializers.ModelSerializer):
    election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all())

    class Meta:
        model = Position
        fields = ['id', 'title', 'description', 'election']
        read_only_fields = ['id']

    def create(self, validated_data):
        return Position.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.election = validated_data.get('election', instance.election)
        instance.save()
        return instance
    
