import requests

from django.shortcuts import render

from .models import City
from .forms import CityForm


def index(request):
    appid='c56398aa9dd4ea5e0854302e39acf5a5'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}&units=metric'

    cities = City.objects.all() # Получаем все данные их базы
    all_cities = [] #* Общий список данных о погоде для передачи на фронт

    if request.method == 'POST':
        form = CityForm(request.POST) #* Форма для вывода на фронт
        form.save()

    form = CityForm() # Очищаем форму

    for city in cities:
        weather_response = requests.get(url=url.format(city=city.name, appid=appid))
        if weather_response.status_code != 200 or 'error' in weather_response.json():
            weather_json = weather_response.json()
            city_info = {
                'city': 'Произошла ошибка',
                'temp': None,
                'icon': weather_json['error']
            }
        elif weather_response.json():
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
        context={'all_info': all_cities, 'form': form},
    )
