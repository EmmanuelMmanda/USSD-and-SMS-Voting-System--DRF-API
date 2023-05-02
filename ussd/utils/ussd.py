from django.test import RequestFactory
from voting.views import VotersDetailView
from voting.views import CandidateListView
from voting.views import ElectionPositionsView
from ussd.utils.Menus import USSDMenu
from ussd.utils.ussd_response import USSDResponseHandler
from rest_framework.request import Request

from voting.views.Settings_view import getSeetingsByUser
from .resultHandller import Results


request_factory = RequestFactory()
request = request_factory.get('/')

class USSDVoting:
    def __init__(self,request):
        self.voter = VotersDetailView()
        self.candidates = CandidateListView()
        self.positions = ElectionPositionsView()
        self.lang = self.get_settings_by_user(self.voter)
        self.menu = USSDMenu(self.lang)
        self.response = USSDResponseHandler(self.lang)

    

    def getCandidates(self):
        response = self.candidates.get(request, 1)
        candidates_data = response.data
        return candidates_data

    def USSDHandler(self, text, session_id, phone_number):
        # Check if the voter is registered
        is_registered = self.voter.is_registered(phone_number)
        # has_voted = self.voter.has_voted(phone_number)
        has_voted = False

        # Split USSD input text
        text_array = text.split('*')
        level = len(text_array)
        response = ''

        # Handle USSD input based on user registration status and text input
        if is_registered and text == '':
            return self.menu.MainMenu()
        elif not is_registered:
            return self.response.NotRegisteredErrorMenu()
        elif text_array[0] == '1':
            # Handle vote casting
            if not has_voted:
                if level == 1:
                    position = 'Chairperson' if self.menu.lang == 'EN' else 'Mwenyekiti'
                    response = self.menu.VoteMenu(
                        position, 1, self.getCandidates())
                elif level == 2:
                    if not text_array[1].isdigit() or int(text_array[1]) not in [1, 2]:
                        response = self.response.invalid_input()
                    else:
                        position = 'Vice Chairperson' if self.menu.lang == 'EN' else 'Makamu Mwenyekiti'
                        response = self.menu.VoteMenu(
                            position, 2, self.getCandidates())
                elif level == 3:
                    if not text_array[1].isdigit() or int(text_array[1]) not in [1, 2, 3]:
                        response = self.response.invalid_input()
                    else:
                        position = 'Secretary' if self.menu.lang == 'EN' else 'Katibu'
                        response = self.menu.VoteMenu(
                            position, 3, self.getCandidates())
                elif level == 4:
                    if not text_array[1].isdigit() or int(text_array[1]) not in [1, 2, 3, 4]:
                        response = self.response.invalid_input()
                    else:
                        position = 'Treasurer' if self.menu.lang == 'EN' else 'Mweka Hazina'
                        response = self.menu.VoteMenu(
                            position, 4, self.getCandidates())
                elif level == 5:
                    if not all(map(str.isdigit, text_array[1:])):
                        response = self.response.invalid_input()
                    else:
                        response = self.menu.BallotMenu(text_array)
                elif level == 6:
                    last_text = text_array[-1]
                    if last_text == '1':
                        try:
                            self.cast_vote(phone_number, text_array[1:])
                            response = self.response.VoteCastSuccess()
                        except:
                            response = self.response.VoteCastError()
                    elif last_text == '2':
                        response = self.menu.MainMenu()
                    else:
                        response = self.response.invalid_input()
                else:
                    response = self.response.Error()

                return (response)
            else:
                return self.response.AlreadyVotedResponse()

        elif text_array[0] == '2':
            # Handle viewing results
            response = self.view_results()
            return (response)

        elif text_array[0] == '3':
            # try change language
            try:
                usersettings = self.get_settings_by_user(self.voter__user)
                if usersettings.language == 'EN':
                    self.lang = 'SW'
                    response = self.menu.changeLanguageSuccess()
                else:
                    self.lang = 'EN'
            except:
                response = self.response.Error()

            return (response)
        else:
            response = self.response.invalid_input()
            return (response)

        # Check for invalid input
        if level > 6:
            response = self.response.invalid_input()
        return response

    def cast_vote(self, phone_number, candidate_number):
        # send a post request to the API to cast the vote based on our Voting app
        return None

    def view_results(self):
        results = Results()
        ArusoResults = results.get_results(1, request)
        
        return self.response.resultMenu(ArusoResults)
    
    def get_settings_by_user(self,user):
        try:
            settings = getSeetingsByUser()
            userSettings = settings.get(user=user)

            return userSettings
        except:
            return 'Error fetching user settings'
        

