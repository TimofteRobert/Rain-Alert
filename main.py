# Get the weather data for the next 12 hours
import requests
from twilio.rest import Client
import os


# Set the OpenWeatherMap API endpoint and API key
OWM_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "ACb0d2a7a5d5e4e0b0d2a7a5d5e4e0b0d"
auth_token = os.environ.get("TWI_AUTH_TOKEN")


# Set the latitude and longitude of your city
weather_params = {
    "lat": 45.752361,
    "lon": 22.896049,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

# Check if it will rain in the next 12 hours
will_rain = False

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]
for hour_data in weather_slice:
    # Get the condition code from the weather data
    condition_code = hour_data["weather"][0]["id"]
    # Check if the condition code indicates rain
    if int(condition_code) < 700:
        will_rain = True

# If it will rain, send an SMS to the user
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an umbrella!",
        from_="+1234567890",
        to="your number"
    )
    print(message.status)
