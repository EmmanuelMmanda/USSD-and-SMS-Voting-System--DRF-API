from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from voting.auth import IsSuperuserOrReadOnly
from voting.models import Position
from voting.serializers.PositionSerializer import PositionSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly


# get list of all positions based on election id
class ElectionPositionsView(APIView):
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]

    def get(self, request, election_id, format=None):
        positions = Position.objects.filter(election_id=election_id)
        serializer = PositionSerializer(positions, many=True)
        if not serializer.data:
            data = {
                "detail": "No positions found",
                "status": status.HTTP_404_NOT_FOUND,
                "data": serializer.data
            }
            return Response(data)
        data = {
            "detail": "Positions retrieved successfully",
            "status": status.HTTP_200_OK,
            "data": serializer.data
        }
        return Response(data)

    def post(self, request, election_id, format=None):
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "detail": "Position created successfully",
                "status": status.HTTP_201_CREATED,
                "data": serializer.data
            }
            return Response(data)
        data = {
            "detail": "Error creating position",
            "status": status.HTTP_400_BAD_REQUEST,
            "data": serializer.errors
        }
        return Response(data)


# get position based on election id and position id
class ElectionPositionsDetailView(APIView):
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]

    def get_object(self, election_id, position_id):
        try:
            return Position.objects.get(pk=position_id, election_id=election_id)
        except Position.DoesNotExist:
            raise Http404("Position does not exist")

    def get(self, request, election_id, position_id, format=None):
        try:
            position = self.get_object(election_id, position_id)
            serializer = PositionSerializer(position)
            return Response({'data': serializer.data, 'status': status.HTTP_200_OK, 'detail': 'success'})
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Position not found'})

    def put(self, request, election_id, position_id, format=None):
        try:
            position = self.get_object(election_id, position_id)
            serializer = PositionSerializer(position, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data, 'status': status.HTTP_200_OK, 'detail': 'success'})
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'Invalid request data'})
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Position not found'})

    def delete(self, request, election_id, position_id, format=None):
        try:
            position = self.get_object(election_id, position_id)
            position.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'detail': 'Position deleted successfully'})
        except Http404:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Position not found'})
