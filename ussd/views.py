from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ussd.middlewares import USSDMiddleware

class USSDView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # Call the USSD middleware to handle the request and get the response
        middleware = USSDMiddleware(get_response=None)
        response = middleware(request)

        # Return the response
        return response

