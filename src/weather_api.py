import requests
import json

def get_weather_json(lat=25.07, lon=121.57):

    # temperature_2m -> temperature
    # apparent_temperature -> feels_like
    # relative_humidity_2m -> humidity
    # wind_speed_10m -> wind_speed
    # precipitation -> precipitation
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current = data['current']

        weather_output = {
            "temperature": current['temperature_2m'],
            "feels_like": current['apparent_temperature'],
            "humidity": current['relative_humidity_2m'],
            "wind_speed": current['wind_speed_10m'],
            "precipitation": current['precipitation']
        }

        return weather_output

    except Exception as e:
        return {"error": str(e)}