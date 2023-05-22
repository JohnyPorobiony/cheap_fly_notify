from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager

flight_search = FlightSearch()
data_manager = DataManager()
notification = NotificationManager()

data_manager.update_destination_codes(flight_search)

for city in data_manager.destination_data:
    # Search for a direct connection
    flight = flight_search.search_for_flight(city["iataCode"], 0)
    # Search for connection with one stopover
    if flight is None:
        flight = flight_search.search_for_flight(city["iataCode"], 2)
        if flight is None:
            continue
    # Check if the connection is cheaper than the lowest connection in Google Sheet
    new_occasion = data_manager.check_and_update_prices(flight)
    if new_occasion:
        for user in data_manager.users_data:
            notification.send_email(flight, user["email"])
