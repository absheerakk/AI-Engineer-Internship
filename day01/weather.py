'''
    Exercise 2 — Get Current Weather
        ● API: OpenWeatherMap (free tier) — openweathermap.org
        ● Task: Sign up for a free API key, then fetch the current weather for your city. Print the temperature, humidity, and description.
        ● Bonus: Convert the temperature from Kelvin to Celsius.

'''
import requests

API_KEY = "36be7937ed3ac1c319741aa341bfc7ce" 
CITY_NAME = "Calicut"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric"

response = requests.get(url)

if response.status_code == 200:
    data = response.json() #another, and might be preferred method to convert to jason
    
    city = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"] #getting element from a dictonary inside a list
    
    # Display the structured data
    print(f"Weather in {city}:")
    print(f"Temperature: {temp}°C")
    print(f"Temperature in kelvin: {temp+273.15}K")
    print(f"Humidity: {humidity}%")
    print(f"Conditions: {description.capitalize()}")
else:
    print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
