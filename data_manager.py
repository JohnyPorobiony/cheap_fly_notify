import requests
from dotenv import load_dotenv
import os
load_dotenv()

SHEETY_API_KEY = os.getenv('SHEETY_API_KEY')
SHEETY_END = f"https://api.sheety.co/{SHEETY_API_KEY}/flightDeals"
SHEETY_TOKEN = os.getenv('SHEETY_TOKEN')
SHEETY_HEADERS = {"Authorization": f"Bearer {SHEETY_TOKEN}",
                  "Content-Type": "application/json"}


class DataManager:
    """This class is responsible for managing the data in the Google Sheet"""

    def __init__(self):
        self.destination_data = self.get_destination_data()
        self.users_data = self.get_users_data()

    def get_users_data(self):
        """This method is responsible for getting data for each user from Google Sheets"""
        url = f"{SHEETY_END}/users"
        response_sheety = requests.get(url=url, headers=SHEETY_HEADERS)
        response_sheety.raise_for_status()
        self.users_data = response_sheety.json()["users"]
        return self.users_data
    
    def get_destination_data(self):
        """This method is responsible for getting data for each destination from Google Sheets"""
        url = f"{SHEETY_END}/prices"
        response_sheety = requests.get(url=url, headers=SHEETY_HEADERS)
        response_sheety.raise_for_status()
        self.destination_data = response_sheety.json()["prices"]
        return self.destination_data

    def update_destination_codes(self, flight_search):
        """This method is responsible for updating each IATA Codes in Google Sheets with the data from the Google Sheets"""
        for city in self.destination_data:
            try:
                city["iataCode"]
            except KeyError:
                city["iataCode"] = flight_search.get_destination_code(city["city"])
                end = f"{SHEETY_END}/prices/{city['id']}"
                city = {"price": {"iataCode": city["iataCode"]}}
                updated_sheety = requests.put(url=end, headers=SHEETY_HEADERS, json=city)
                updated_sheety.raise_for_status()
            else:
                if city["iataCode"] == "":
                    city["iataCode"] = flight_search.get_destination_code(city["city"])
                    end = f"{SHEETY_END}/prices/{city['id']}"
                    city = {"price": {"iataCode": city["iataCode"]}}
                    updated_sheety = requests.put(url=end, headers=SHEETY_HEADERS, json=city)
                    updated_sheety.raise_for_status()
                    
        print("IATA Codes updated")

    def check_and_update_prices(self, flight):
        """This method is responsible for checking/updating the lowest price for given flight in the Google Sheets"""
        for city in self.destination_data:
            # If the flight's price is lower than price in Google Sheet -> update it and return True    
            if flight.price_PLN < city["lowestPrice"] and flight.arrival_airport_code == city["iataCode"]:
                end = f"{SHEETY_END}/prices/{city['id']}"
                row = {"price": {"lowestPrice": flight.price_PLN}}
                updated_sheety = requests.put(url=end, headers=SHEETY_HEADERS, json=row)
                updated_sheety.raise_for_status()
                print(f"{city['city']} Lowest Price updated from {city['lowestPrice']} to {flight.price_PLN}")
                return True

    def add_new_user(self):
        """This method is responsible for adding new user to the Google Sheets"""
        url = f"{SHEETY_END}/users"
        first_name = input("Welcome to Flight Finder!\nPlease enter your first name:\n")
        last_name = input("Please enter your last name:\n")
        email = input("Enter your email address:\n")
        email2 = input("Enter your email address again to confirm:\n")

        if email == email2:
            data = {"user": {"firstName": first_name,
                             "lastName": last_name,
                             "email": email}}
            response_sheety_users = requests.post(url=url, headers=SHEETY_HEADERS, json=data)
            response_sheety_users.raise_for_status()
            self.users_data = self.get_users_data()
            print(f"{email} added to the database") 
        else:
            print("Entered emails have to be identical.")

    def add_new_destination(self):
        """This method is responsible for adding new destination City to the Google Sheets"""
        url = f"{SHEETY_END}/prices"
        city = input("What city would you like to fly to? \n")
        max = input("How much do you want to spend maximum?\n")
        data = {"price": {"city": city,
                          "iataCode": "",
                          "lowestPrice": int(max)}}
        response_sheety_prices = requests.post(url=url, headers=SHEETY_HEADERS, json=data)
        response_sheety_prices.raise_for_status()
        self.destination_data = self.get_destination_data()
        print(f"{city} added to the database")
