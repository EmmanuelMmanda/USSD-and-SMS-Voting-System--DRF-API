# manage the imports
from rest_framework import serializers
from voting.models import Vote
from voting.models import Voter
from voting.models import Candidate
from .PositionSerializer import PositionSerializer
from .ElectionSerializer import ElectionSerializer



class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote

        fields = "__all__"

        read_only_fields = ['id']
