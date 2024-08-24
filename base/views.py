from django.shortcuts import render, redirect
from .forms import WeatherSearchForm, EmailSubscriptionForm
from .models import WeatherHistory, EmailSubscription
from django.core.mail import send_mail
from django.conf import settings
import requests
import json

# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.crypto import get_random_string

API_KEY = settings.API_KEY
API_URL = settings.API_URL
# Create your views here.
def home(request):
    if request.method == 'POST':
        form = WeatherSearchForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            response = requests.get(f"{API_URL}/current.json?key={API_KEY}&q={city}")
            forecast_response = requests.get(f"{API_URL}/forecast.json?key={API_KEY}&q={city}&days=5")
            if response.status_code == 200:
                data = response.json()
                forecast_data = forecast_response.json()
                current_weather = {
                    'city': data['location']['name'],
                    'date': data['location']['localtime'],
                    'temperature': data['current']['temp_c'],
                    'wind_speed': data['current']['wind_kph'],
                    'humidity': data['current']['humidity'],
                    'description': data['current']['condition']['text'],
                    'icon': data['current']['condition']['icon']
                }
                forecast_weather = forecast_data['forecast']['forecastday'][1:]
                # Save weather history
                WeatherHistory.objects.create(
                    city=current_weather['city'],
                    temperature=current_weather['temperature'],
                    wind_speed=current_weather['wind_speed'],
                    humidity=current_weather['humidity'],
                    description=current_weather['description']
                )
                context = {
                    'current_weather': current_weather,
                    'forecast_weather': forecast_weather,
                    'form': form
                }
                return render(request, 'home.html', context)
    else:
        form = WeatherSearchForm()
    return render(request, 'home.html', {'form': form})

def weather_by_location(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if lat and lon:
        response = requests.get(f"{API_URL}/forecast.json?key={API_KEY}&q={lat},{lon}&days=5")
        if response.status_code == 200:
            weather_data = response.json()
            current_weather = {
                'city': weather_data['location']['name'],
                'date': weather_data['location']['localtime'],
                'temperature': weather_data['current']['temp_c'],
                'wind_speed': weather_data['current']['wind_kph'],
                'humidity': weather_data['current']['humidity'],
                'description': weather_data['current']['condition']['text'],
                'icon': weather_data['current']['condition']['icon']
            }
            forecast_weather = weather_data['forecast']['forecastday'][1:]
            return render(request, 'home.html', {
                'current_weather': current_weather, 
                'forecast_weather': forecast_weather
                })
        else:
            return render(request, 'error.html', {
                'error_message': 'Unable to retrieve weather data. Please try again.'
                })
    else:
        return render(request, 'error.html', {
            'error_message': 'Location not provided.'
            })

def load_more_forecast(request, city, days):
    try:
        response = requests.get(f"{API_URL}/forecast.json?key={API_KEY}&q={city}&days={days}")
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            return render(request, 'error.html', {
                'error_message': data['error']['message']
                })

        forecast = data['forecast']['forecastday']
        next_days = days + 3 
        return render(request, 'forecast.html', {
            'forecast': forecast, 
            'city': city, 
            'next_days': next_days
            })

    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred: {e}"
        return render(request, 'error.html', {
            'error_message': error_message
            })

# def subscribe(request):
#     if request.method == 'POST':
#         form = EmailSubscriptionForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             confirmation_code = get_random_string(length=32)
#             subscription = EmailSubscription(email=email, confirmation_code=confirmation_code)
#             subscription.save()
#             current_site = get_current_site(request)
#             confirmation_link = f"http://{current_site.domain}/confirm/{confirmation_code}"
#             send_mail(
#                 'Confirm your subscription',
#                 f'Please confirm your subscription by clicking the link: {confirmation_link}',
#                 settings.EMAIL_HOST_USER,
#                 [email],
#                 fail_silently=False,
#             )
#             return redirect('home')
#     else:
#         form = EmailSubscriptionForm()
#     return render(request, 'weather/subscribe.html', {'form': form})

# def confirm_subscription(request, confirmation_code):
#     try:
#         subscription = EmailSubscription.objects.get(confirmation_code=confirmation_code, is_confirmed=False)
#         subscription.is_confirmed = True
#         subscription.save()
#         # Send a welcome email or some sort of notification
#     except EmailSubscription.DoesNotExist:
#         # Handle invalid confirmation code
#         pass
#     return redirect('home')
