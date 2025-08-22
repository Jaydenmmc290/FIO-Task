from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime as dt
import requests

# Home
def index(request):
    return render(request, "app/index.html")

# Function to request weather data
def request_to_WeatherAPI(city):
    URL = f"http://api.weatherapi.com/v1/forecast.json?key={settings.WA_API_KEY}&q={city}&days=5"
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()



 # Current weather
    last_updated_str = data["current"]["last_updated"]  
    last_updated_dt = dt.strptime(last_updated_str, "%Y-%m-%d %H:%M")

    current =  {
        "city": data["location"]["name"],
        "description": data["current"]["condition"]["text"],
        "icon": f'http:{data["current"]["condition"]["icon"]}',
        "temperature": data["current"]["temp_c"],
        "updated_date": dt.fromtimestamp(data["current"]["last_updated_epoch"]),
        "api_response": response.text
    }

     # 5 days wether 
    forecast = []
    for day in data["forecast"]["forecastday"]:
        forecast.append({
            "date": day["date"],
            "max_temp": day["day"]["maxtemp_c"],
            "min_temp": day["day"]["mintemp_c"],
            "description": day["day"]["condition"]["text"],
            "icon": f'http:{day["day"]["condition"]["icon"]}'
        })

    return {
        "current": current,
        "forecast": forecast
        }


def trigger(request):
    city = request.GET.get("city")
    if not city:
        return JsonResponse({"error": "City parameter is required"}, status=400)

    try:
        weather_data = request_to_WeatherAPI(city)
        return JsonResponse(weather_data)
    except requests.HTTPError as e:
        return JsonResponse({"error": f"HTTP error: {e}"}, status=500)
    except Exception as e:
        
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": f"Unexpected error: {e}"}, status=500)