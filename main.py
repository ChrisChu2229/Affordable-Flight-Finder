from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
from datetime import datetime, timedelta
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "SFO"

FlightSearch = FlightSearch()
DataManager = DataManager()
NotificationManager = NotificationManager()

sheet_data = DataManager.get_destination_data()
user_emails = DataManager.get_email_address()
pprint(user_emails)

if sheet_data[0]["iataCode"] == "":
    print("filling in empty iataCode")
    for cityItem in sheet_data:
        cityItem['iataCode'] = FlightSearch.getIataCode(cityItem['city'])

    print("retrieved IATA codes")
    pprint(sheet_data)

    DataManager.destination_data = sheet_data
    DataManager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(180))

for destination in sheet_data:
    max_stopovers_count = 0
    flight = FlightSearch.searchCheapestFlight(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today,
        max_stopovers=max_stopovers_count
    )

    while not flight:
        max_stopovers_count += 1
        flight = FlightSearch.searchCheapestFlight(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_months_from_today,
            max_stopovers=max_stopovers_count
        )
    if flight and flight.price < destination["lowestPrice"]:
        NotificationManager.sendText(flight.price, "San Francisco", ORIGIN_CITY_IATA, flight.destination_city,
                                     flight.destination_airport, flight.out_date, flight.return_date, max_stopovers_count, flight.via_city_to, flight.via_city_from)
        for user in user_emails:
            NotificationManager.sendEmail(user["email"], flight.price, "San Francisco", ORIGIN_CITY_IATA, flight.destination_city,
                                     flight.destination_airport, flight.out_date, flight.return_date, max_stopovers_count, flight.via_city_to, flight.via_city_from)
    # elif flight and flight.price < destination["lowestPrice"]:
    #     NotificationManager.sendText(flight.price, "San Francisco", ORIGIN_CITY_IATA, flight.destination_city,
    #                                  flight.destination_airport, flight.out_date, flight.return_date,
    #                                  max_stopovers_count, flight.via_city_to, flight.via_city_from)
    #     for user in user_emails:
    #         NotificationManager.sendEmail(user["email"], flight.price, "San Francisco", ORIGIN_CITY_IATA,
    #                                       flight.destination_city,
    #                                       flight.destination_airport, flight.out_date, flight.return_date,
    #                                       max_stopovers_count, flight.via_city_to, flight.via_city_from)





