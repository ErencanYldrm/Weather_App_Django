from django.shortcuts import redirect, render
import requests
from .models import City
from .forms import CityForm


def home(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=f960d50e283cb9ae7475ea657d2186d9"

    cities = City.objects.all()

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    form = CityForm()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json()

        weather = {
            'city': city,
            'temperature': round(((city_weather['main']['temp']-32)*5/9), 2),
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}

    return render(request, "index.html", context)


def clear(request):
    City.objects.all().delete()
    return redirect("home")
