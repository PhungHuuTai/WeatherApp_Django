from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('load_more/<str:city>/<int:days>/', views.load_more_forecast, name='load_more_forecast'),
    path('weather_by_location/', views.weather_by_location, name='weather_by_location'),
    
]