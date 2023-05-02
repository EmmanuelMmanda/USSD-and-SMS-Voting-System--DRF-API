from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly



class IndexView(APIView):
    permission_classes = [ IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        data = {
            "detail": "Hello, world. You're at the Voting/Polls index.",
            'status': status.HTTP_200_OK,
            "timed_at": timezone.now(),
        }
        return Response(data)
