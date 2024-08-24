from django.contrib import admin
from .models import EmailSubscription, WeatherHistory


# Register your models here.
admin.site.register(EmailSubscription)
admin.site.register(WeatherHistory)
