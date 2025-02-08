from __future__ import print_function
import africastalking

class SMS:
    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key
        africastalking.initialize(self.username, self.api_key)
        self.sms = africastalking.SMS

    def send(self, message, recipients):
        try:
            response = self.sms.send(message, recipients)
            print(response)
            return response
        except Exception as e:
            print(f'Encountered an error while sending: {e}')
            return None



    
