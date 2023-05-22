# cheap_fly_notify

Python / Tequila.Kiwi API / Sheety API program searching for cheap flights (with Tequila.Kwi API) to the locations passed to the Google Sheets document (accessed with Sheety API).

Program searches for direct flight from the Home City with the given parameters (both set in: flight_search.py). If direct flight is not available it searches for the flight with one (or more) stopover.

Program requires following enviroment variables to be set:
  *SHEETY_API_KEY=your_api_key
  *SHEETY_TOKEN=your_token
  *TEQUILA_API_KEY=your_api_key
  *EMAIL=your@email.com
  *EMAIL_APP_PASSWORD=your_password

There are to methods (unimplemented in main.py) for:
  *Adding new user (new email address to send notification)
  *Adding new destination City with maximum affordable ticket cost
  
https://tequila.kiwi.com/
https://sheety.co/
