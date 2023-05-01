from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from voting.models import Election, Voter
from voting.serializers.ElectionSerializer import ElectionSerializer
from rest_framework.permissions import IsAdminUser


class ElectionsListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        elections = Election.objects.all()
        serializer = ElectionSerializer(elections, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ElectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update an election data


class ElectionDetailView(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Election.objects.get(pk=pk)
        except Election.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        election = self.get_object(pk)
        serializer = ElectionSerializer(election)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        election = self.get_object(pk)
        serializer = ElectionSerializer(election, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        election = self.get_object(pk)
        election.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
