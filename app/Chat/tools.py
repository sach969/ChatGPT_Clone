import httpx
import os

WEATHER_API_KEY = os.getenv("weather_api_key")
def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = httpx.get(url)
        data = response.json()
        return f"The weather in {city} is {data['weather'][0]['description']} with a temperature of {data['main']['temp']}°C"
    except: 
        return "Sorry, I couldn't retrieve the weather data at the moment."