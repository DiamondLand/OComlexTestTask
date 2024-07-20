import requests

from django.shortcuts import render


def index(request):
    token='89a0ebedfa3a05c7f1384f2de25ea2e6'
    appid='82b797b6ebc625032318e16f1b42c016'
    url = 'https://samples.openweathermap.org/data/2.5/weather?q={city}&appid={appid}'
    city = 'Moscow'

    weather_response = requests.get(url=url.format(city=city, appid=appid))
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
            'city': city,
            'temp': round(weather_json['main']['temp'] - 273.15, 1),
            'icon': weather_json['weather'][0]['icon']
        }

    return render(
        request=request,
        template_name='weather/index.html',
        context={'info': city_info}
    )
