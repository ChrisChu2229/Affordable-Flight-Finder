import os
from twilio.rest import Client

ACCOUNT_SID = os.environ["TWILIOACCOUNTSID"]
AUTH_TOKEN = os.environ["TWILIOAUTHTOKEN"]


class NotificationManager:

    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)


    def sendText(self, price, departure_city_name, departure_iata_code, arrival_city, arrival_iata_code, outbound_date, inbound_date):
        textMessage = f"Low price alert! Only ${price} to fly from {departure_city_name}-{departure_iata_code} to {arrival_city}-{arrival_iata_code} from {outbound_date} to {inbound_date}."

        message = self.client.messages.create(
            body=textMessage,
            from_="+18444361546",
            to="+14087817022"
        )

        print(message.sid)
