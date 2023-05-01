# views for candidates
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from voting.models import Candidate
from voting.serializers.CandidateSerializer import CandidateSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly


# get list of all candidates based on an election id
class CandidateListView(APIView):
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]

    def get(self, request, election_id, format=None):
        candidates = Candidate.objects.filter(
            position__election__id=election_id)
        serializer = CandidateSerializer(candidates, many=True)
        return Response({'candidates': serializer.data, 'status': status.HTTP_200_OK, 'detail': 'Candidates retrieved successfully'})

    def post(self, request, election_id, format=None):
        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': status.HTTP_201_CREATED, 'detail': 'Candidate created successfully'})
        return Response({'data': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST, 'detail': 'Failed to create candidate'})


# get a specific candidate based on an election id and a candidate id


class CandidateDetailView(APIView):
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]

    def get_object(self, election_id, candidate_id):
        try:
            return Candidate.objects.get(position__election__id=election_id, id=candidate_id)
        except Candidate.DoesNotExist:
            raise Http404

    def get(self, request, election_id, candidate_id, format=None):
        candidate = self.get_object(election_id, candidate_id)
        serializer = CandidateSerializer(candidate)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK, 'detail': 'Candidate retrieved successfully'})

    def put(self, request, election_id, candidate_id, format=None):
        candidate = self.get_object(election_id, candidate_id)
        serializer = CandidateSerializer(candidate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': status.HTTP_200_OK, 'detail': 'Candidate updated successfully'})
        return Response({'data': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST, 'detail': 'Failed to update candidate'})

    # for partial updates
    def patch(self, request, election_id, candidate_id, format=None):
        candidate = self.get_object(election_id, candidate_id)
        serializer = CandidateSerializer(
            candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status': status.HTTP_200_OK, 'detail': 'Candidate updated successfully'})
        return Response({'data': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST, 'detail': 'Failed to update candidate'})

    def delete(self, request, election_id, candidate_id, format=None):
        candidate = self.get_object(election_id, candidate_id)
        candidate.delete()
        return Response({'status': status.HTTP_204_NO_CONTENT, 'detail': 'Candidate deleted successfully'})
