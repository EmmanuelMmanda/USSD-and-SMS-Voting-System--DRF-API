class USSDResponseHandler:
    def __init__(self, lang):
        self.lang = lang

    def invalid_input(self):
        if self.lang == 'EN':
            error = "END Invalid input or choice, Please try again !\n"
            return error
        elif self.lang == 'SW':
            error = "END Uingizaji usio sahihi, Tafadhali jaribu tena !\n"
            return error

    def VoteCastError(self):
        if self.lang == 'EN':
            error = "END Sorry, there seems to be a problem with your Vote Casting!"
            return error
        elif self.lang == 'SW':
            error = "END Samahani, kuna tatizo na upigaji kura wako!"
            return error

    def VoteCastSuccess(self):
        if self.lang == 'EN':
            message = "END Your Voting process is Accomplished."
            message += "You will receive a confirmation SMS Shortly."
            return message
        elif self.lang == 'SW':
            message = "END Maombi yako ya kupiga kura yamepokelewa."
            message += "Utapokea SMS ya uthibitisho hivi karibuni."
            return message

    def Success(self):
        if self.lang == 'EN':
            message = "END Success"
            return message
        elif self.lang == 'SW':
            message = "END Imefanikiwa"
            return message

    def Error(self):
        if self.lang == 'EN':
            error = "END Error"
            return error
        elif self.lang == 'SW':
            error = "END Kosa"
            return error

    def SMSMessage(self):
        if self.lang == 'EN':
            message = "END Your vote has been casted successfully"
            return message
        elif self.lang == 'SW':
            message = "END Kura yako imepigwa kwa mafanikio"
            return message

    def IncorrectPIN(self):
        if self.lang == 'EN':
            error = "END Incorrect PIN, Please try again"
            return error
        elif self.lang == 'SW':
            error = "END PIN sio sahihi, Tafadhali jaribu tena"
            return error

    def NotRegisteredErrorMenu(self):
        if self.lang == 'EN':
            return ('END Sorry, You are not allowed to participate in this election! '
                    'Please contact the election administrator for more information \n'
                    )
        elif self.lang == 'SW':
            return ('END Samahani, huwezi kushiriki katika uchaguzi huu! '
                    'Tafadhali wasiliana na msimamizi wa uchaguzi kwa maelezo zaidi \n'
                    )

    def AlreadyVotedResponse(self):
        if self.lang == 'EN':
            return ('END Sorry, You have already voted! in this Election ! '
                    'You can View results only \n'
                    )
        elif self.lang == 'SW':
            return ('END Samahani, umeshapiga kura ! '
                    'Unaweza kuona matokeo tu \n'
                    )
    
    def resultMenu(self, results):
        if self.lang == 'EN':
            menu = f"END Voting Results: \n Name - votes - percentage\n _______________________________\n"
            for result in results:
                menu += f"{result['candidate_full_name']} - {result['vote_count']} - {round(result['vote_percentage'])}%\n"
            menu += f"_______________________________\n"
            menu += f"An SMS will be sent to you with the results."
            return menu
        
        elif self.lang == 'SW':
            menu = f"END Matokeo ya Kura: \n Jina - kura - asilimia\n _______________________________\n"
            for result in results:
                menu += f"{result['candidate_full_name']} - {result['vote_count']} - {round(result['vote_percentage'])}%\n"
            menu += f"_______________________________\n"
            menu += f"SMS itatumwa kwako na matokeo."
            return menu
        
