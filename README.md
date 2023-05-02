# Affordable Flight Finder

Affordable Flight Finder is a Python application that helps users find the cheapest flights from San Francisco (SFO) to various destinations. The application leverages the power of the Tequila API and Google Sheets to store and manage flight data. When a cheaper flight is found, the user is notified via a text message using the Twilio API.

## Project Structure

The project is composed of several Python files, each with its purpose:

- `main.py`: The main entry point for the application, which utilizes all the other classes.
- `flight_data.py`: Defines the `FlightData` class, a simple data structure to hold information for a single flight.
- `data_manager.py`: Handles accessing and updating data from Google Sheets using the Sheety API.
- `flight_search.py`: Interacts with the Tequila API to search for the cheapest flights and retrieve IATA codes for cities.
- `notification_manager.py`: Sends text messages using the Twilio API when a cheaper flight is found.

## How it works

1. The application starts by fetching the destination data from Google Sheets using the `DataManager` class. If any of the cities are missing IATA codes, the application retrieves them using the Tequila API through the `FlightSearch` class and updates Google Sheets accordingly.
2. The application then searches for the cheapest flights between San Francisco (SFO) and each destination city within a specified date range (from tomorrow to six months from now) using the `FlightSearch` class.
3. If a flight is found with a price lower than the recorded lowest price in Google Sheets, the `NotificationManager` class sends a text message to the user with the flight details.
4. (Optional) The application can update the lowest price for each destination in the Google Sheets using the `DataManager` class. (This feature is currently commented out in `main.py`)

## Setup

1. Clone the repository.
2. Set up your own Tequila API account [here](https://tequila.kiwi.com/portal/login) and get your API key.
3. Set up your own Twilio account [here](https://www.twilio.com/try-twilio) and get your Account SID and Auth Token.
4. Create your own Google Sheets with flight data, following the format of the example sheet provided in the project repository.
- should look like this:
![image](https://user-images.githubusercontent.com/92602228/235743025-ff81828c-ba4e-412f-8046-4b6e16871d6e.png)
5. Install the required dependencies:
- pip install requests
- pip install twilio
6. Set up the following environment variables:
- `TEQUILAAPIKEY`: Your Tequila API key.
- `TWILIOACCOUNTSID`: Your Twilio Account SID.
- `TWILIOAUTHTOKEN`: Your Twilio Auth Token.
7. Run the application: `python main.py`


