
class FlightData:
    """This class is responsible for structuring the flight data"""
    def __init__(self):
        self.id = None
        self.price_PLN = None
        self.departure_airport_code = None
        self.departure_city = None
        self.departure_date = None
        self.arrival_city = None
        self.arrival_airport_code = None
        self.back_date = None
        self.airlines = None
        self.flight_no = None
        self.flight_no2 = None
        self.url = None
        self.via_city_code = None
        self.via_city_code2 = None
        self.has_stopovers = False

    def get_flight_data(self, flight):
        """This method is responsible for getting each flight's data"""
        self.id = flight['data'][0]['id']
        self.departure_city = flight['data'][0]['cityFrom']
        self.departure_airport_code = flight['data'][0]['cityCodeFrom']
        self.departure_date = flight['data'][0]['local_departure'].split('T')[0]
        self.arrival_city = flight['data'][0]['cityTo']
        self.arrival_airport_code = flight['data'][0]['cityCodeTo']
        self.back_date = flight['data'][0]['route'][1]['local_departure'].split('T')[0]
        self.price_PLN = flight['data'][0]['price']
        self.airlines = flight['data'][0]['airlines']
        self.flight_no = flight['data'][0]['route'][0]['flight_no']
        self.flight_no2 = flight['data'][0]['route'][1]['flight_no']
        self.url = flight['data'][0]['deep_link']
        if len(flight['data'][0]['route']) == 4:
            self.via_city_code = flight['data'][0]['route'][0]['cityCodeTo']
            self.via_city_code2 = flight['data'][0]['route'][2]['cityCodeTo']
            self.has_stopovers = True
