import smtplib
from dotenv import load_dotenv
import os
load_dotenv()

class NotificationManager:
    """This class is responsible for sending emails"""
    def __init__(self):
        self.sender_email = os.getenv("EMAIL")
        self.password = os.getenv("EMAIL_APP_PASSWORD")

    def send_email(self, flight, user_email):
        """Send an email with the notification"""
        # If the flight is direct
        if flight.via_city_code is not None:
            msg = f"Subject: New occasion!\n\nThere is attractive occasion: From {flight.departure_city} to" \
                  f" {flight.arrival_city} only for {flight.price_PLN} PLN!\n\n\n{flight.url}\n\n" \
                  f"Flights with stopovers:\n{flight.departure_airport_code} -> {flight.via_city_code} -> " \
                  f"{flight.arrival_airport_code}\n{flight.arrival_airport_code} -> {flight.via_city_code2} -> " \
                  f"{flight.departure_airport_code}\n\n".encode('utf-8')
        # If the flight has stopover(s)
        else:
            msg = f"Subject: New occasion!\n\nThere is attractive occasion: From {flight.departure_city} to" \
                  f" {flight.arrival_city} only for {flight.price_PLN} PLN!\n\n\n" \
                  f"{flight.url}\n".encode('utf-8')

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            print(f"sending email -> {user_email}")
            connection.starttls()
            connection.login(user=self.sender_email, password=self.password)
            connection.sendmail(from_addr=self.sender_email,
                                to_addrs=user_email,
                                msg=msg)
            print("email sent\n")
