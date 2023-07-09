import os
import africastalking
from dotenv import load_dotenv  
load_dotenv()

# Initialize Africa's Talking
username = os.getenv('SANDBOX_USER')
api_key = os.getenv('DEV_API_KEY')
africastalking.initialize(username, api_key)   

sms = africastalking.SMS


class SMS():
    def __init__(self):
        pass

    def send(self, recepients, message):
        #check if reipirnts phonenumbers have the 255 country code if not append it 
        #iterate trhought therecepients list and check if the first three characters are 255
        #if not append it 
        print(recepients)

        to_be_sent_recepients = []
        for recepient in recepients:
            if [recepient][0:3] != '255':
                recepient = '+255'+recepient[1:]
            to_be_sent_recepients.append(recepient)
            
        
        recipients = to_be_sent_recepients
        # Set your message
        message = message
        # Set your shortCode or senderId
        sender = os.getenv('GATEWAY_SENDER_ID')

        try:
            response = sms.send(message, recipients, sender)
        except Exception as e:
            print(f'Sorry, we have a problem: {e}')