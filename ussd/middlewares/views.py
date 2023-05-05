import re
from django.http import HttpResponse
from django.contrib.auth.models import User
from ..utils import USSDVoting
from voting.views import getSeetingsByUser


def get_user_by_phone(phone_number):
    """
    Get the user from the Django User model based on the phone number.
    """
    try:
        user = User.objects.get(voter__phone_number=phone_number)
        return user
    except User.DoesNotExist:
        return None


def normalize_phone_number(phone_number):

    # Remove the country code prefix if present
    if phone_number.startswith('+255'):
        phone_number = phone_number[4:]
    elif phone_number.startswith('255'):
        phone_number = phone_number[3:]
    elif phone_number.startswith('0'):
        phone_number = phone_number[1:]
    else:
        raise ValueError(' Invalid phone number')

    # Add the "07" prefix to the phone number
    formatted_phone_number = '07' + phone_number[1:]

    return formatted_phone_number


class USSDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            # Get the parameters from the request
            session_id = request.POST.get('sessionId')
            phone_number = request.POST.get('phoneNumber')
            text = request.POST.get('text')

            # check if the parameteres are empty and return a get response
            if session_id == None or phone_number == None or text == None:
                return self.get_response(request)
            # normalize the phone number to append the country code if not present
            try:
                # Normalize the phone number
                phone_number = normalize_phone_number(phone_number)
            except ValueError as e:
                # Return an error response if the phone number is invalid
                response = HttpResponse(f'Error: {str(e)}')
                response['Content-Type'] = 'text/plain'
                return response

             # Get the user by phone number
            user = get_user_by_phone(phone_number)

            # Check if user exists and get the first one
            if not user:
                # User doesn't exist, return an error response
                response = HttpResponse('User not found')
                response['Content-Type'] = 'text/html'
                return response
            print(f'my user->{user.id}')
            # get user preferences and setting
            settings = getSeetingsByUser()
            userSettings = settings.get(request, user.id).data

            # Append the user to the USSD response
            ussd_handler = USSDVoting(request, userSettings).USSDHandler
            ussd_response = ussd_handler(
                text, session_id, phone_number, user)

            # Return the response with content type set to text/html
            response = HttpResponse(ussd_response)
            response['Content-Type'] = 'text/html'
            return response

        return self.get_response(request)
