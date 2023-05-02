from django.test import RequestFactory
from ussd.utils.ussd_response import USSDResponseHandler
from voting.views import GenerateResultsView
from voting.views import ResultsListView
from rest_framework.response import Response
from .ussd_response import USSDResponseHandler

resultMenu = USSDResponseHandler('EN').resultMenu
request_factory = RequestFactory()
request = request_factory.get('/')
response = ''


class Results:
    def __init__(self):
        self.results = ResultsListView()
        self.generate_results = GenerateResultsView()

    def get_results(self, election_id, request):
        # get results view from the voting app
        self.generate_results.post(request)
        res = self.results.get(request, election_id)
        return res.data
