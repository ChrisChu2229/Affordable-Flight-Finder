import os
import smtplib
from twilio.rest import Client

ACCOUNT_SID = os.environ["TWILIOACCOUNTSID"]
AUTH_TOKEN = os.environ["TWILIOAUTHTOKEN"]
GMAIL_PASSWORD = os.environ["GMAILPASSWORD"]
MYPHONENUMBER = os.environ["MYPHONENUMBER"]
MYEMAIL = os.environ["MYEMAIL"]


class NotificationManager:

    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def sendText(self, price, departure_city_name, departure_iata_code, arrival_city, arrival_iata_code, outbound_date,
                 inbound_date, stop_overs, via_city_to, via_city_from):

        if stop_overs:
            textMessage = f"Low price alert! Only ${price} to fly from {departure_city_name}-{departure_iata_code} to {arrival_city}-{arrival_iata_code} from {outbound_date} to {inbound_date}.\n\nFlight has {stop_overs} stop over(s), one to {via_city_to} and one from {via_city_from}."
        else:
            textMessage = f"Low price alert! Only ${price} to fly from {departure_city_name}-{departure_iata_code} to {arrival_city}-{arrival_iata_code} from {outbound_date} to {inbound_date}."

        message = self.client.messages.create(
            body=textMessage,
            from_="+18444361546",
            to=MYPHONENUMBER
        )

        print(message.sid)

    def sendEmail(self, reciever, price, departure_city_name, departure_iata_code, arrival_city, arrival_iata_code, outbound_date,
                 inbound_date, stop_overs, via_city_to, via_city_from):
        sender = MYEMAIL
        subject = "Low airline ticket price found!"

        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        if stop_overs:
            message = f"Low price alert! Only ${price} to fly from {departure_city_name}-{departure_iata_code} to {arrival_city}-{arrival_iata_code} from {outbound_date} to {inbound_date}.\n\nFlight has {stop_overs} stop over(s), one to {via_city_to} and one from {via_city_from}."
        else:
            message = f"Low price alert! Only ${price} to fly from {departure_city_name}-{departure_iata_code} to {arrival_city}-{arrival_iata_code} from {outbound_date} to {inbound_date}."

        with smtplib.SMTP(smtp_server, smtp_port) as server:

            server.starttls()

            username = MYEMAIL
            password = GMAIL_PASSWORD
            server.login(username, password)

            server.sendmail(sender, reciever, f"Subject: {subject}\n\n{message}")

            server.quit()


