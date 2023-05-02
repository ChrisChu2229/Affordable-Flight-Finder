# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests as requests
import os
from twilio.rest import Client
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import FlightData
from datetime import datetime, timedelta
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "SFO"

FlightSearch = FlightSearch()
DataManager = DataManager()
# FlightData = FlightData()
NotificationManager = NotificationManager()


sheet_data = DataManager.get_destination_data()

# # This code is for retrieving the IATA code if there is none there, the Google sheets data is now populated so this
# code is unnecessary ## pprint(sheet_data) ##

if sheet_data[0]["iataCode"] == "":
    print("filling in empty iataCode")
    for cityItem in sheet_data:
        cityItem['iataCode'] = FlightSearch.getIataCode(cityItem['city'])

    print("retrieved IATA codes")
    pprint(sheet_data)

    DataManager.destination_data = sheet_data
    DataManager.update_destination_codes()

# my attempt at finding the cheapest flight but all the work was being done in flight; I did all the logic inside
# the search the cheapest flight function but now the logic has been split up ##
# for cityItem in sheet_data:
#     cityItem["lowestPrice"] = FlightData.searchCheapestFlight("San Francisco", 1000, cityItem["iataCode"])

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(180))

for destination in sheet_data:
    flight = FlightSearch.searchCheapestFlight(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today
    )
    if flight and flight.price < sheet_data[0]["lowestPrice"]:
        NotificationManager.sendText(flight.price, "San Francisco", ORIGIN_CITY_IATA, flight.destination_city, flight.destination_airport, flight.out_date, flight.return_date)

# DataManager.destination_data = sheet_data
# DataManager.update_price()


