# manage the imports
from rest_framework import serializers
from voting.models import Results


class ResultsSerializer(serializers.ModelSerializer):
    position_title = serializers.SerializerMethodField()
    candidate_full_name = serializers.SerializerMethodField()

    def get_position_title(self, obj):
        return obj.position.title

    def get_candidate_full_name(self, obj):
        return obj.candidate.first_name + " " + obj.candidate.last_name

    class Meta:
        model = Results
        fields = ['id', 'election', 'position', 'position_title', 'candidate',
                  'candidate_full_name', 'vote_count', 'vote_percentage']
        read_only_fields = ['id']

    def create(self, validated_data):
        return Results.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.election = validated_data.get('election', instance.election)
        instance.position = validated_data.get('position', instance.position)
        instance.candidate = validated_data.get(
            'candidate', instance.candidate)
        instance.vote_count = validated_data.get(
            'vote_count', instance.vote_count)
        instance.vote_percentage = validated_data.get(
            'vote_percentage', instance.vote_percentage)
        instance.save()
        return instance
