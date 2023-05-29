import json
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from voting.models import Vote
from voting.serializers.VoteSerializer import VoteSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class VotesListView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response({'data': serializer.data, 'message': 'Votes retrieved successfully.', 'status': status.HTTP_200_OK})

    permission_classes = [IsAdminUser | IsAuthenticated]
    def post(self, request, format=None):
        print(f'vote-> {request.data}')
        for vote in request.data:
            try:
                serializer = VoteSerializer(data=vote)
            except Exception as e:
                print(f'error-> {e}')
            if serializer.is_valid():
                #set voter status to voted
                voter = serializer.validated_data['voter']
                voter.has_vote = True
                voter.save()
                serializer.save()
            
            else:
                return Response({'error': serializer.errors, 'message': 'Error creating vote.', 'status': status.HTTP_400_BAD_REQUEST})
        return Response({'message': 'Votes created successfully.', 'status': status.HTTP_201_CREATED})
    
class VotesDetailView(APIView):
    permission_classes = [IsAdminUser ]

    def get_object(self, pk):
        try:
            return Vote.objects.get(pk=pk)
        except Vote.DoesNotExist:
            raise Http404

    def get(self, request, vote_id, format=None):
        vote = self.get_object(vote_id)
        serializer = VoteSerializer(vote)
        return Response({'data': serializer.data, 'message': 'Vote retrieved successfully.', 'status': status.HTTP_200_OK})

    def put(self, request, vote_id, format=None):
        vote = self.get_object(vote_id)
        serializer = VoteSerializer(vote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Vote updated successfully.', 'status': status.HTTP_200_OK})
        return Response({'data': serializer.errors, 'message': 'Error updating vote.', 'status': status.HTTP_400_BAD_REQUEST})

    def delete(self, request, vote_id, format=None):
        vote = self.get_object(vote_id)
        vote.delete()
        return Response({'message': 'Vote deleted successfully.', 'status': status.HTTP_204_NO_CONTENT})


# get votes for a particular election
class VotesForElectionView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Vote.objects.get(pk=pk)
        except Vote.DoesNotExist:
            raise Http404

    def get(self, request, election_id, format=None):
        votes = Vote.objects.filter(ballot__election__id=election_id)
        serializer = VoteSerializer(votes, many=True)
        return Response({'data': serializer.data, 'message': 'Votes for election retrieved successfully.', 'status': status.HTTP_200_OK})
