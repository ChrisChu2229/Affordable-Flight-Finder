import os
from pprint import pprint

from flight_data import FlightData
import requests
from notification_manager import NotificationManager

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com/"
TEQUILA_API_KEY = os.environ["TEQUILAAPIKEY"]
NotificationManager = NotificationManager()


class FlightSearch:

    def getIataCode(self, city):
        endpoint = f"{TEQUILA_ENDPOINT}locations/query"
        headers = {
            "apikey": TEQUILA_API_KEY,
        }
        query = {
            "term": city, "location_types": "city"
        }
        response = requests.get(url=endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        print(response.status_code)
        iataCode = results[0]["code"]
        print("retrieving iata code for", city)
        print("iataCode is", iataCode)
        return iataCode

    def searchCheapestFlight(self, origin_city_code, destination_city_code, from_time, to_time, max_stopovers):
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": max_stopovers,
            "curr": "USD"
        }

        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}v2/search",
            headers=headers,
            params=query
        )

        try:
            data = response.json()["data"][0]
            if max_stopovers > 0:
                pprint(data)
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        if max_stopovers > 0:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                stop_overs=max_stopovers,
                via_city_to=data["route"][0]["cityTo"],
                via_city_from=data["route"][2]["cityTo"]
            )
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
            )
        print(f"{flight_data.destination_city}: ${flight_data.price}")
        return flight_data
