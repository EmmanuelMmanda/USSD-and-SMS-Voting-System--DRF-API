from django.test import RequestFactory
from voting.views import VotersDetailView
from voting.views import CandidateListView
from voting.views import ElectionPositionsView
from voting.views import SettingsDetailView
from ussd.utils.Menus import USSDMenu
from ussd.utils.ussd_response import USSDResponseHandler
from rest_framework.request import Request

from voting.views.Settings_view import getSeetingsByUser
from .resultHandller import Results

from .sms import SMS


request_factory = RequestFactory()
request = request_factory.get('/')


class USSDVoting:
    def __init__(self, request, UserPrefs):
        self.voter = VotersDetailView()
        self.candidates = CandidateListView()
        self.positions = ElectionPositionsView()
        self.lang = UserPrefs[0]['language'] if UserPrefs else 'EN'
        self.settingDetail = SettingsDetailView()
        self.userPrefs = UserPrefs
        self.menu = USSDMenu(self.lang)
        self.response = USSDResponseHandler(self.lang)
        self.sms = SMS()

    def getCandidates(self):
        response = self.candidates.get(request, 1)
        candidates_data = response.data
        return candidates_data

    def USSDHandler(self, text, session_id, phone_number, user):
        print(f'USSDHandler-> {text}')
        # Check if the voter is registered
        is_registered = self.voter.is_registered(phone_number)
        has_voted = False

        print(f'phonenumber at ussd.py-> {phone_number}')

        # check if go back or main menu is selected
        # self.go_back_main_menu(text)

        # print(f'is_registered-> {is_registered}')
        # self.go_back(text)

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
                        position, 1, self.getCandidates())
                elif level == 2:
                    if not text_array[1].isdigit() or int(text_array[1]) not in [1, 2, 98, 99]:
                        response = self.response.invalid_input()
                    else:
                        position = 'Vice Chairperson' if self.menu.lang == 'EN' else 'Makamu Mwenyekiti'
                        response = self.menu.VoteMenu(
                            position, 2, self.getCandidates())
                elif level == 3:
                    if not text_array[2].isdigit() or int(text_array[2]) not in [3, 4, 98, 99]:
                        response = self.response.invalid_input()
                    else:
                        position = 'Secretary' if self.menu.lang == 'EN' else 'Katibu'
                        response = self.menu.VoteMenu(
                            position, 3, self.getCandidates())
                elif level == 4:
                    if not text_array[3].isdigit() or int(text_array[3]) not in [5, 6, 98, 99]:
                        response = self.response.invalid_input()
                    else:
                        position = 'Treasurer' if self.menu.lang == 'EN' else 'Mweka Hazina'
                        response = self.menu.VoteMenu(
                            position, 4, self.getCandidates())
                elif level == 5:
                    if not text_array[4].isdigit() or int(text_array[4]) not in [7, 8, 98, 99]:
                        response = self.response.invalid_input()
                    else:
                        response = self.menu.BallotMenu(request, text_array)
                elif level == 6:
                    last_text = text_array[-1]
                    if last_text == '1':
                        try:
                            res = self.cast_vote(phone_number, text_array[1:])
                            if res:
                                try:
                                    self.sms.send(
                                        [phone_number], self.response.SMSMessage())
                                except Exception as e:
                                    response = self.response.Error() + str(e)
                            response = self.response.VoteCastSuccess()
                        except Exception as e:
                            response = self.response.VoteCastError() + str(e)
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
            # try change language
            currentLang = self.lang
            if currentLang == 'EN':
                self.lang = 'SW'
            else:
                self.lang = 'EN'
            try:
                self.settingDetail.change_language(request,
                                                   self.userPrefs[0]['id'], self.lang)
                response = self.menu.changeLanguageSuccess()
            except Exception as e:
                response = self.response.Error() + str(e)
            return (response)
        else:
            print('invalid input')
            response = self.response.invalid_input()
            return (response)

        # Check for invalid input
        if level > 6:
            response = self.response.invalid_input()
        return response

    def cast_vote(self, phone_number, candidate_number):
        # send a post request to the API to cast the vote based on our Voting app
        return True

    def view_results(self):
        results = Results()
        ArusoResults = results.get_results(1, request)

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
