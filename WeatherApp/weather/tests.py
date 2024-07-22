from django.test import TestCase, Client
from django.urls import reverse

from .models import City
from .forms import CityForm


class WeatherViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
        self.city_name = 'Moscow'
        City.objects.create(name=self.city_name)

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/index.html')
        self.assertIsInstance(response.context['form'], CityForm)
        self.assertIn('all_info', response.context)
        self.assertGreater(len(response.context['all_info']), 0)

    def test_post_request(self):
        new_city = 'London'
        response = self.client.post(self.url, {'name': new_city})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(City.objects.filter(name=new_city).exists())

    def test_weather_info_in_template(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.city_name)
