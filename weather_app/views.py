from django.shortcuts import render
import requests
import datetime
from config.api_key import OPENWEATHERMAP_API_KEY

def WeatherApp(request):
    api_key = OPENWEATHERMAP_API_KEY
    
    current_weather_data_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
    
    forecast_data_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}&units=metric'
    
    
    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2',None)
        
        weather_data1 , daily_forecast_data1 = fetch_weather_forecast(city1,api_key,current_weather_data_url,forecast_data_url)
        
        if city2:
            weather_data2 , daily_forecast_data2 = fetch_weather_forecast(city2,api_key,current_weather_data_url,forecast_data_url)
        else:
            weather_data2 , daily_forecast_data2 = None, None
        
        context = {
            'weather_data1': weather_data1,
            'daily_forecast_data1': daily_forecast_data1,
            'weather_data2': weather_data2,
            'daily_forecast_data2': daily_forecast_data2,
        }
        
        return render(request, 'weather_app/index.html', context)
        
    else:
        return render(request, 'weather_app/index.html')
    

def fetch_weather_forecast(city,api_key,current_weather_data_url,forecast_data_url):
    weather_data = requests.get(current_weather_data_url.format(city,api_key)).json()
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    
    forecast_data = requests.get(forecast_data_url.format(lat,lon,api_key)).json()
    
    weather_data_response = {
        'city': city,
        'temperature': weather_data['main']['temp'],
        'description': weather_data['weather'][0]['description'],
        'icon': weather_data['weather'][0]['icon'],
    }
    
    daily_forecasts = []
    
    for daily_data in forecast_data['daily'][:5]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': daily_data['temp']['min'],
            'max_temp': daily_data['temp']['max'],
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })
        
    return weather_data_response, daily_forecasts