from django.db import models

# Create your models here.
class WeatherHistory(models.Model):
    city = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    temperature = models.FloatField()
    wind_speed = models.FloatField()
    humidity = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Weather in {self.city} on {self.date}"

class EmailSubscription(models.Model):
    email = models.EmailField(unique=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.email
