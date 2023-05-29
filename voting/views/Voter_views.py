from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from voting.serializers.VoterSerializer import VoterSerializer
from voting.models import Election, Voter
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly


class VotersListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        try:
            voters = Voter.objects.all()
        except Voter.DoesNotExist:
            return Response({"detail": "Voters not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VoterSerializer(voters, many=True)
        data = {
            "data": serializer.data,
            "detail": "Voters retrieved successfully",
            "status": status.HTTP_200_OK
        }
        return Response(data)

    def post(self, request, format=None):
        serializer = VoterSerializer(data=request.data)

        


        if serializer.is_valid():

            serializer.save()
            data = {
                "data": serializer.data,
                "detail": "Voter created successfully",
                "status": status.HTTP_201_CREATED
            }
            return Response(data)
        data = {
            "data": serializer.errors,
            "detail": "Error creating voter",
            "status": status.HTTP_400_BAD_REQUEST
        }
        return Response(data)


class VotersDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return Voter.objects.get(pk=pk)

    def get(self, request, voter_id, format=None):
        try:
            voter = self.get_object(voter_id)
        except Voter.DoesNotExist:
            return Response({"detail": "Voters not found !", "status" :status.HTTP_404_NOT_FOUND})

        serializer = VoterSerializer(voter)
        data = {
            "data": serializer.data,
            "detail": "Voter retrieved successfully",
            "status": status.HTTP_200_OK
        }
        return Response(data)

    def put(self, request, voter_id, format=None):
        try:
            voter = self.get_object(voter_id)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = VoterSerializer(voter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": serializer.data,
                "detail": "Voter updated successfully",
                "status": status.HTTP_200_OK
            }
            return Response(data)
        data = {
            "data": serializer.errors,
            "detail": "Error updating voter",
            "status": status.HTTP_400_BAD_REQUEST
        }
        return Response(data)

    def delete(self, request, voter_id, format=None):
        try:
            voter = self.get_object(voter_id)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        voter.delete()
        data = {
            "detail": "Voter deleted successfully",
            "status": status.HTTP_204_NO_CONTENT
        }
        return Response(data)

    def patch(self, request, voter_id, format=None):
        try:
            voter = self.get_object(voter_id)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = VoterSerializer(voter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "data": serializer.data,
                "detail": "Voter updated successfully",
                "status": status.HTTP_200_OK
            }
            return Response(data)
        data = {
            "data": serializer.errors,
            "detail": "Error updating voter",
            "status": status.HTTP_400_BAD_REQUEST
        }
        return Response(data)
    
     # get voter by phone number
    def is_registered(self, phone_number):
        try:
            voter = Voter.objects.get(phone_number=phone_number)
            if voter:
                print(f"Voter is {voter}")
                return True
            else:
                return False
        except Voter.DoesNotExist:
            print("voter does not exist")
            return False
        
    def get_voter(self, phone_number):
        try:
            voter = Voter.objects.get(phone_number=phone_number)
            if voter:
                return voter
            else:
                return None
        except Voter.DoesNotExist:
            print("voter does not exist")
            return None

    def has_voted(self, phone_number):
        try:
            voter = Voter.objects.get(phone_number=phone_number)
            if voter.has_vote:
                return True
            else:
                return False
        except Voter.DoesNotExist:
            print("voter does not exist")
            return False
