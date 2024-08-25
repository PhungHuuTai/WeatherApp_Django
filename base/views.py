from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import WeatherSearchForm, EmailSubscriptionForm
from .models import WeatherHistory, EmailSubscription
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.auth.tokens import default_token_generator as token_generator
from .tokens import EmailConfirmationTokenGenerator
import requests
import json

token_generator = EmailConfirmationTokenGenerator()

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

def subscribe(request):
    if request.method == 'POST':
        form = EmailSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscription, created = EmailSubscription.objects.get_or_create(email=email)
            if created or not subscription.is_confirmed:
                subscription.save()
                
                token = token_generator.make_token(subscription)
                uid = urlsafe_base64_encode(force_bytes(subscription.pk))
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                http_content = render_to_string('activation_email.html', {
                    'user': subscription,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                msg = EmailMessage(mail_subject, http_content, settings.EMAIL_HOST_USER, [subscription.email])
                msg.content_subtype = 'html'
                msg.send()

                return render(request, 'confirmed.html', {
                    'message': 'Please confirm your email address to complete the registration.'
                    })
            elif subscription.is_confirmed:
                return render(request, 'confirmed.html', {
                    'message': 'You are already subscribed and confirmed.'
                    })
            else:
                return render(request, 'confirmed.html', {
                    'message': 'This email is already registered but not confirmed. Please check your inbox for the confirmation email.'
                })
    else:
        form = EmailSubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        subscription = EmailSubscription.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, EmailSubscription.DoesNotExist):
        subscription = None

    if subscription is not None and token_generator.check_token(subscription, token):
        subscription.is_confirmed = True
        subscription.save()
        return render(request, 'confirmed.html', {'message': 'Your email has been confirmed!'})
    else:
        return render(request, 'confirmed.html', {'message': 'Activation link is invalid!'})

def unsubscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        subscription = EmailSubscription.objects.filter(email=email).first()
        if subscription:
            subscription.delete()
            messages.success(request, 'You have successfully unsubscribed.')
        else:
            messages.error(request, 'Email not found or already unsubscribed.')
        return redirect('home')
    return render(request, 'unsubscribe.html')
