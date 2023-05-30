import json
from django.urls import reverse
import requests
from voting.views import VotersDetailView
from voting.views import CandidateListView
from voting.views import ElectionPositionsView
from voting.views import SettingsDetailView
from ussd.utils.Menus import USSDMenu
from ussd.utils.ussd_response import USSDResponseHandler
from rest_framework.request import Request
from rest_framework.authtoken.models import Token


from voting.views.Settings_view import getSeetingsByUser
from voting.views.Vote_views import VotesListView
from .resultHandller import Results

from .sms import SMS


class USSDVoting:
    def __init__(self, request, UserPrefs, BASE_URL):
        self.voter = VotersDetailView()
        self.candidates = CandidateListView()
        self.positions = ElectionPositionsView()
        self.vote = VotesListView()
        self.lang = UserPrefs[0]['language'] if UserPrefs else 'EN'
        self.settingDetail = SettingsDetailView()
        self.userPrefs = UserPrefs
        self.menu = USSDMenu(self.lang)
        self.response = USSDResponseHandler(self.lang)
        self.sms = SMS()
        self.request = request
        self.BASE_URL = BASE_URL

    def getCandidates(self, request):
        response = self.candidates.get(self.request, 1)
        candidates_data = response.data
        return candidates_data

    def USSDHandler(self, text, session_id, phone_number, user):
        print(f'USSDHandler-> {text}')
        # Check if the voter is registered
        is_registered = self.voter.is_registered(phone_number)
        # Check if the voter has voted
        has_voted = self.voter.has_voted(phone_number)

        print(f'phonenumber at ussd.py-> {phone_number}')
        # Split USSD input text by asterisk
        text_array = text.split('*')

        # Get the length of the text array
        level = len(text_array)
        print(f'level-> {level}')
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
                        position, 1, self.getCandidates(self.request))
                elif level == 2:
                    if not text_array[1].isdigit() or int(text_array[1]) not in [1, 2, 3, 98, 99]:
                        response = self.response.invalid_input()
                    else:
                        position = 'Vice Chairperson' if self.menu.lang == 'EN' else 'Makamu Mwenyekiti'
                        response = self.menu.VoteMenu(
                            position, 2, self.getCandidates(self.request))
                elif level == 3:
                    if not text_array[2].isdigit() or int(text_array[2]) not in [4, 5, 6, 98, 99]:
                        response = self.response.invalid_input()
                    else:
                        response = self.menu.BallotMenu(
                            self.request, text_array)
                elif level == 4:
                    last_text = text_array[-1]
                    if last_text == '1':
                        res = self.cast_vote(phone_number, text_array[1:])
                        print(f'res-> {res}')
                        if res:
                            print(f'sending sms ...{phone_number}')
                            self.sms.send(
                                        [phone_number], self.response.SMSMessage())
                            response = self.response.VoteCastSuccess()
                        else:
                            response = self.response.VoteCastError()
                    elif last_text == '2':
                        print('user pressed 2')
                        response = self.response.cancelRequestResponse()
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
            print('changing language ...')
            # try change language
            currentLang = self.lang
            if currentLang == 'EN':
                self.lang = 'SW'
            else:
                self.lang = 'EN'
            try:
                print(f'currentLang-> {currentLang} -usrpresf-> {self.userPrefs}')
                self.settingDetail.change_language(self.request,
                                                   self.userPrefs[0]['id'], self.lang)
                response = self.menu.changeLanguageSuccess()
            except Exception as e:
                response = self.response.Error() + str(e)
            return (response)
        else:
            print('invalid input')
            response = self.response.invalid_input()
            return (response)

    def cast_vote(self, phone_number, data):
        # Get the voter's details
        voter = self.voter.get_voter(phone_number)
        print(f'voter-> {voter.user}')
        token = Token.objects.get(user=voter.user)

        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Token {token}'}

        votes = [
            {
                "voter": voter.id,
                "Position": 1,
                "candidate": data[0]
            },
            {
                "voter": voter.id,
                "Position": 2,
                "candidate": data[1]
            }
        ]
        url = f'{self.BASE_URL}votes/'
        json_data = json.dumps(votes)
        voting = requests.post(url, data=json_data, headers=headers)
        if voting.status_code == 201 or voting.status_code == 200:
            return True
        return False

    def view_results(self):
        results = Results()
        ArusoResults = results.get_results(1, self.request)

        return self.response.resultMenu(ArusoResults)

    def go_back_main_menu(self, text):
        print(f'go_back_main_menu-> {text}')
        # remove the existing text and text array ib our session
        exploded_text = text.split('*')
        if "99" in exploded_text is not False:
            first_index = exploded_text.index(
                exploded_text) if "99" in exploded_text else -1
            exploded_text = exploded_text[first_index +
                                          1:] if first_index != -1 else exploded_text
            text = '*'.join(exploded_text)

    def go_back(self, text):
        print(f'go_back-> {text}')
        # remove the existing text and text array ib our session
        exploded_text = text.split('*')
        if "98" in exploded_text is not False:
            first_index = exploded_text.index(
                exploded_text) if "98" in exploded_text else -1
            exploded_text = exploded_text[first_index +
                                          1:] if first_index != -1 else exploded_text
            text = '*'.join(exploded_text)
        return text
