import requests

from django.shortcuts import render
from .models import City


def index(request):
    appid='89a0ebedfa3a05c7f1384f2de25ea2e6'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}&units=metric'

    cities = City.objects.all()
    all_cities = []

    for city in cities:
        weather_response = requests.get(url=url.format(city=city.name, appid=appid))

        if weather_response.status_code != 200 or 'error' in weather_response.json():
            weather_json = weather_response.json()
            city_info = {
                'city': 'Произошла ошибка',
                'temp': None,
                'icon': weather_json['error']
            }
        else:
            weather_json = weather_response.json()
            city_info = {
                'city': city.name,
                'temp': weather_json['main']['temp'],
                'icon': weather_json['weather'][0]['icon']
            }
    
        all_cities.append(city_info)

    return render(
        request=request,
        template_name='weather/index.html',
        context={'all_info': all_cities}
    )
