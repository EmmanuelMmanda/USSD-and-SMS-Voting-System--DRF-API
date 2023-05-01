from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from voting.models import Ballot
from voting.serializers.BallotSerializer import BallotSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly


class BallotsListView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        ballots = Ballot.objects.all()
        serializer = BallotSerializer(ballots, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BallotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BallotsDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Ballot.objects.get(pk=pk)
        except Ballot.DoesNotExist:
            raise Http404

    def get(self, request, ballot_id, format=None):
        ballot = self.get_object(ballot_id)
        serializer = BallotSerializer(ballot)
        return Response(serializer.data)

    def put(self, request, ballot_id, format=None):
        ballot = self.get_object(ballot_id)
        serializer = BallotSerializer(ballot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ballot_id, format=None):
        ballot = self.get_object(ballot_id)
        ballot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#get ballots for a particular election
class BallotsForElectionView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Ballot.objects.get(pk=pk)
        except Ballot.DoesNotExist:
            raise Http404


    def get(self, request, election_id, format=None):
        ballots = Ballot.objects.filter(election_id=election_id)
        serializer = BallotSerializer(ballots, many=True)
        return Response(serializer.data)

