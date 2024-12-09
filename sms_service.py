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

if __name__ == '__main__':
    # Initialize the SMS service with your credentials
    username = "davidas"  
    api_key = "atsk_770cdbd4bfcc606a586c95d34c13e5576b07bb7ffe3fc04f43fad4e4882130bbb869415f"
    sms_service = SMS(username, api_key)

    # Example message to be sent
    message = "Thank you for using our services!"

    # Recipients' phone numbers will be dynamically handled in the Flask app
