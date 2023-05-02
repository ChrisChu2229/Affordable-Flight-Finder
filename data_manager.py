import requests

SHEETY_ENDPOINT = "https://api.sheety.co/b6bc9e4a849142592866117161926671/flightDealFinder/prices"



class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):

        response = requests.get(url=SHEETY_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]

        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price" : {
                    "iataCode" : city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)

    def update_price(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                        "lowestPrice": city["lowestPrice"]
                    }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)
