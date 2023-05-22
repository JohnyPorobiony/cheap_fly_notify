import requests
from datetime import datetime, timedelta
from flight_data import FlightData
from dotenv import load_dotenv
import os
load_dotenv()

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = os.getenv("TEQUILA_API_KEY")
TEQUILA_HEADERS = {"apikey": TEQUILA_API_KEY, "content type": "application/json"}


HOME = "WAW"  # Your home city IATA Code


class FlightSearch:
    """This class is responsible for getting data and searching for flights with Tequila-Kiwi API"""
    def get_destination_code(self, city_name):
        """This method is responsible for getting and returning IATA Codes"""
        query = {"term": city_name}
        response_tequila = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query",
                                        headers=TEQUILA_HEADERS,
                                        params=query)
        response_tequila.raise_for_status()
        destination_code = response_tequila.json()["locations"][0]["code"]
        print(f"Getting code: {destination_code}")
        return destination_code

    def search_for_flight(self, fly_to, stopovers):
        """This method is responsible for searching flights"""

        tomorrow = datetime.today() + timedelta(days=1)
        tomorrow_formatted = tomorrow.strftime("%d/%m/%Y")
        three_months_later = tomorrow + timedelta(days=90)
        three_months_later_formatted = three_months_later.strftime("%d/%m/%Y")

        query = {
            "fly_from": HOME,
            "fly_to": fly_to,
            "date_from": tomorrow_formatted,
            "date_to": three_months_later_formatted,
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 7,
            "flight_type": "round",
            "curr": "PLN",
            "max_stopovers": stopovers
        }

        url = f"{TEQUILA_ENDPOINT}/v2/search"
        response_tequila = requests.get(url=url,
                                        headers=TEQUILA_HEADERS,
                                        params=query)
        response_tequila.raise_for_status()
        flight_data = response_tequila.json()

        flight = FlightData()

        try:
            flight.get_flight_data(flight_data)
        except IndexError:
            print(f"No direct flights found to the airport with code:{fly_to}!")
            return None
        else:
            print(f"{flight.departure_city} ✈️ {flight.arrival_city} for {flight.price_PLN}💲")
            if flight.has_stopovers:
                print(f"Flights with stopovers:\n{flight.departure_airport_code} -> {flight.via_city_code} -> {flight.arrival_airport_code}\n{flight.arrival_airport_code} -> {flight.via_city_code2} -> {flight.departure_airport_code}")
            return flight
