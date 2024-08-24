from django import forms
from .models import EmailSubscription

class WeatherSearchForm(forms.Form):
    city = forms.CharField(label='Enter a city name', max_length=100)

class EmailSubscriptionForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ['email']
