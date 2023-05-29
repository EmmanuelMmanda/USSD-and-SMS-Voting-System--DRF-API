import re
from django.http import HttpResponse
from django.contrib.auth.models import User

from voting.views.Settings_view import SettingsDetailView
from ..utils import USSDVoting
from voting.views import getSeetingsByUser, SettingsView
from ussd.utils.ussd_response import USSDResponseHandler


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

            # generate a base url
            BASE_URL = request.build_absolute_uri('/')

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
            # create a new language setings for the user

            # Check if user exists and get the first one
            if not user:
                # User doesn't exist, return an error response
                response = HttpResponse(
                    'END Oops! You are not allowed to participate in electios, Please contact the administrator to register you.')
                response['Content-Type'] = 'text/html'
                return response
            # get user preferences and setting
            settings = getSeetingsByUser()
            userSettings = settings.get(request, user.id).data

            # check if no alnguage settings for the user and create one
            if not userSettings:
                # create a new language setings for the user
                SettingsDetailView().addDefaultLang(request, user.id)
                # get user preferences and setting
                userSettings = settings.get(request, user.id).data

            # Append the user to the USSD response
            ussd_handler = USSDVoting(
                request, userSettings, BASE_URL).USSDHandler
            ussd_response = ussd_handler(
                text, session_id, phone_number, user)

            print(f'ussd_response->{ussd_response}')

            # Return the response with content type set to text/html
            response = HttpResponse(ussd_response)
            response['Content-Type'] = 'text/html'
            return response

        return self.get_response(request)
