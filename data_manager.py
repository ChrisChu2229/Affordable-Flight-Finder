import requests
import os

SHEETY_ENDPOINT_PRICES = os.environ["SHEETYENDPOINTPRICES"]
SHEETY_ENDPOINT_USERS = os.environ["SHEETYENDPOINTUSERS"]


class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.user_email_address = {}

    def get_destination_data(self):

        response = requests.get(url=SHEETY_ENDPOINT_PRICES)
        data = response.json()
        self.destination_data = data["prices"]

        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT_PRICES}/{city['id']}",
                json=new_data
            )
            print(response.text)

    def get_email_address(self):

        response = requests.get(url=SHEETY_ENDPOINT_USERS)
        data = response.json()
        self.user_email_address = data["users"]

        return self.user_email_address

