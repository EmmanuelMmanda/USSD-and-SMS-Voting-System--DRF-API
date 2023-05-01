from rest_framework import serializers
from voting.models import Ballot, Voter
from .VoterSerializer import VoterSerializer


class BallotSerializer(serializers.ModelSerializer):
    voter = serializers.PrimaryKeyRelatedField(source='voter.id', read_only=True)

    class Meta:
        model = Ballot
        fields = ['id', 'voter', 'election']
        read_only_fields = ['id']



