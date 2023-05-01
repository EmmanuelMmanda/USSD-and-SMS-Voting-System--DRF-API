#manage the imports 
from rest_framework import serializers
from voting.models import Election


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ['id', 'title', 'description', 'start_date', 'end_date']
