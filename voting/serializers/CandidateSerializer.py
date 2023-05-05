#manage the imports 
from rest_framework import serializers
from voting.models import Candidate
from voting.models import Position


class CandidateSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())
    position__title = serializers.CharField(source='position.title', read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'first_name', 'last_name', 'manifesto', 'position', 'position__title']

    def get_position(self, obj):
        return obj.position.title

    def create(self, validated_data):
        return Candidate.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.manifesto = validated_data.get('manifesto', instance.manifesto)
        instance.position = validated_data.get('position', instance.position)
        instance.save()
        return instance
    
    #for patch method
    def partial_update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.manifesto = validated_data.get('manifesto', instance.manifesto)
        instance.position = validated_data.get('position', instance.position)
        instance.save()
        return instance

    
