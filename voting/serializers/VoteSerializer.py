# manage the imports
from rest_framework import serializers
from voting.models import Vote
from voting.models import Voter
from voting.models import Ballot
from voting.models import Candidate
from .PositionSerializer import PositionSerializer
from .ElectionSerializer import ElectionSerializer



class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote

        fields = "__all__"

        read_only_fields = ['id']

    # def create(self, validated_data):
    #     return Vote.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.voter = validated_data.get('voter', instance.voter)
    #     instance.ballot = validated_data.get('ballot', instance.ballot)
    #     instance.position = validated_data.get('position', instance.position)
    #     instance.candidate = validated_data.get(
    #         'candidate', instance.candidate)
    #     instance.time_cast = validated_data.get(
    #         'time_cast', instance.time_cast)
    #     instance.vote_value = validated_data.get(
    #         'vote_value', instance.vote_value)
    #     instance.save()
    #     return instance
