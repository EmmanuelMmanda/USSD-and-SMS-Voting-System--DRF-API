from django.http import HttpResponse
from django.test import RequestFactory
from ..utils import USSDVoting
import re
from django.contrib.auth.models import User
from voting.views import getSeetingsByUser


request_factory = RequestFactory()
request = request_factory.get('/')
USSDHandler = USSDVoting(request).USSDHandler

# get user by phone number from django user model


def get_user_by_phone(phone_number):
    try:
        user = User.objects.get(voter__phone_number=phone_number)
        return user
    except User.DoesNotExist:
        return None


class PhoneNumber:
    def __init__(self, number):
        self.number = number

    def is_valid(self):
        return bool(re.match(r'^(\+?255|0)[67]\d{8}$', self.number))

    def normalize(self):
        if self.number.startswith('0'):
            return self.number
        elif self.number.startswith('255'):
            return '0' + self.number[3:]
        elif self.number.startswith('+255'):
            return '0' + self.number[4:]
        else:
            raise ValueError(
                'Invalid phone number format provided for %s' % self.number)


class USSDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            session_id = request.POST.get('sessionId')
            phone_number = request.POST.get('phoneNumber')
            text = request.POST.get('text')

            phone = PhoneNumber(phone_number)
            if not phone.is_valid():
                # Invalid phone number format, return an error response
                response = HttpResponse('Invalid phone number format')
                return response

            phone_number = phone.normalize()

            ussd_response = USSDHandler(text, session_id, phone_number)
            response = HttpResponse(ussd_response)
            response['Content-Type'] = 'text/plain'
            user = get_user_by_phone(phone_number)
            settings = get_settings_by_user(user)

            request.session['settings'] = settings
            request.session['user'] = user

            return response

        return self.get_response(request)
