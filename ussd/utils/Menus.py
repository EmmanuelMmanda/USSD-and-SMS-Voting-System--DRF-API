import json
from django.http import QueryDict
from voting.views import get_candidates_by_ids_with_positions
from typing import List, Dict


class USSDMenu:
    def __init__(self, lang):
        self.lang = lang

    def get_menu(self, text):
        if self.lang == 'EN':
            return f"CON {text} \n"
        elif self.lang == 'SW':
            return f"CON {text} \n"

    def PINMenu(self):
        return self.get_menu('Please enter your PIN/Password')

    def MainMenu(self):
        if self.lang == 'EN':
            return self.get_menu('Welcome to Ardhi University Voting System \n'
                                 '1. Cast your Vote \n'
                                 '2. View Results \n'
                                 '3. Badili Lugha \n')
        elif self.lang == 'SW':
            return self.get_menu('Karibu katika mfumo wa kupiga kura - Chuo Cha Ardhi \n'
                                 '1. Piga kura yako \n'
                                 '2. Angalia matokeo \n'
                                 '3. Change Language\n')

    def VoteMenu(self, position_name, position_id, candidates):

        menu = self.get_candidates_with_position(position_id, candidates)

        if self.lang == 'EN':
            return self.get_menu(f'Vote for ARUSO {position_name} \n{menu}')
        elif self.lang == 'SW':
            return self.get_menu(f'Piga kura kwa {position_name} wa ARUSO \n {menu}')

    def BallotMenu(self, request, text_array):
        print(text_array)
        # map throug the text array and return the items and add them to a request query params
        id1 = text_array[1]
        id2 = text_array[2]
        id3 = text_array[3]
        id4 = text_array[4]

        # Create a new QueryDict with the updated query parameters
        query_params = QueryDict(mutable=True)
        query_params.update({
            'id1': id1,
            'id2': id2,
            'id3': id3,
            'id4': id4,
        })

        # Replace the existing query parameters in the request with the new QueryDict
        request.GET = query_params

        # get candidates based on thoses specific ids
        getCandidates = get_candidates_by_ids_with_positions()
        candidates = getCandidates.get(request, 1)

        # print(candidates.data)

        # format the candidates
        filtered_candidates = [c for c in candidates.data['candidates']]

        result = [
            f" {c['first_name']} {c['last_name']} - {c['position__title']}" for c in filtered_candidates]

        formatted_string = "\n".join(result)

        if self.lang == 'EN':
            return self.get_menu('You have selected \n '
                                 '____________________________'
                                 f'{formatted_string} \n'
                                 'Please select \n'
                                 '1. Confirm \n'
                                 '2. Cancel \n')
        elif self.lang == 'SW':
            return self.get_menu('Umechagua - \n '
                                 '____________________________'
                                 f'{formatted_string} \n'
                                 'Tafadhali chagua \n'
                                 '1. Thibitisha \n'
                                 '2. Sitisha \n')

    def changeLanguageSuccess(self):
        if self.lang == 'SW':
            return ('END Language changed successfully')
        elif self.lang == 'EN':
            return ('END Lugha imebadilishwa kwa mafanikio')

    def get_candidates_with_position(self, position_id, candidates_json):
        # assume that the JSON response is stored in a variable called candidates_json
        candidates = candidates_json['candidates']

        # filter the candidates by position_id
        filtered_candidates = [
            c for c in candidates if c['position'] == position_id]

        # create a formatted string for each candidate in the form "Candidate A - positionID"
        result = [
            f"{c['id']}. {c['first_name']} {c['==']} " for c in filtered_candidates]

        # create a menu from the result
        menu = ''
        for i, candidate in enumerate(result):
            menu += f"{candidate}\n"

        print(menu)
        return menu
    
    