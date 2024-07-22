import requests

from django.shortcuts import render

from .models import City
from .forms import CityForm


def index(request):
    appid='c56398aa9dd4ea5e0854302e39acf5a5'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}&units=metric'

    cities = City.objects.all() # Получаем все данные их базы
    all_cities = [] #* Общий список данных о погоде для передачи на фронт
    error_message = None

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            city, created = City.objects.get_or_create(name=city_name)
            if not created:
                city.request_count += 1
                city.save()
        else:
            error_message = "Form is not valid. Errors: " + str(form.errors)

    form = CityForm() # Очищаем форму

    for city in cities:
        try:
            weather_response = requests.get(url=url.format(city=city.name, appid=appid))
            weather_response.raise_for_status()
            weather_json = weather_response.json()
            if 'main' in weather_json and 'weather' in weather_json:
                city_info = {
                    'city': city.name,
                    'temp': weather_json['main']['temp'],
                    'icon': weather_json['weather'][0]['icon']
                }
            else:
                city_info = {
                    'city': city.name,
                    'temp': 'N/A',
                    'icon': 'N/A'
                }
        except requests.exceptions.RequestException as _ex:
            error_message = f"Произошла ошибка: {_ex}"
            city_info = {
                'city': city.name,
                'temp': 'N/A',
                'icon': 'N/A'
            }

        all_cities.append(city_info)

    return render(
        request=request,
        template_name='weather/index.html',
        context={'all_info': all_cities, 'form': form, 'error_message': error_message},
    )