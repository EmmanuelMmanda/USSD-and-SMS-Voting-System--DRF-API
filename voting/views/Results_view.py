from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from voting.serializers.ResultsSerializer import ResultsSerializer
from voting.models import Election, Position, Candidate, Vote, Results
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.db import transaction



class ResultsListView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, election_id):
        # Get the election object based on the election_id
        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            return Response({"error": "Election not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all the results for the given election
        results = Results.objects.filter(election=election)

        # Serialize the results
        serializer = ResultsSerializer(results, many=True)

        # Return the serialized results
        return Response(serializer.data)



class GenerateResultsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Get all the elections
            elections = Election.objects.all()
            #get existing results
            results = Results.objects.all()

            with transaction.atomic():
                # Delete all the existing results
                results.delete()

                # Iterate over each election
                for election in elections:
                    # Get all the positions for this election
                    positions = Position.objects.filter(election=election)

                    # Iterate over each position
                    for position in positions:
                        # Get all the candidates for this position
                        candidates = Candidate.objects.filter(position=position)

                        # Count the number of votes for each candidate
                        votes = Vote.objects.filter(Position=position).values(
                            'candidate').annotate(vote_count=Count('candidate'))

                        # Calculate the total number of votes cast
                        total_votes = Vote.objects.filter(Position=position).count()

                        # Iterate over each candidate
                        for candidate in candidates:
                            # Get the number of votes for this candidate
                            vote_count = next(
                                (item['vote_count'] for item in votes if item['candidate'] == candidate.id), 0)

                            # Calculate the percentage of votes for this candidate
                            vote_percentage = vote_count / total_votes * 100 if total_votes > 0 else 0

                            # Create a result object for this candidate
                            result = Results(
                                election=election,
                                position=position,
                                candidate=candidate,
                                vote_count=vote_count,
                                vote_percentage=vote_percentage
                            )

                            # Save the result object to the database
                            result.save()

                #get the updated results 
                results = Results.objects.all()
                serializer = ResultsSerializer(results, many=True)

            # Return a success message
            return Response({'message': 'Results generated successfully', 'results': serializer.data, 'status': status.HTTP_201_CREATED})

        except Exception as e:
            return Response({'message': str(e), 'status': status.HTTP_400_BAD_REQUEST})

    def delete(self, request):
        # Delete all the results
        Results.objects.all().delete()

        # Return a success message
        return Response({'message': 'All results deleted successfully'})
