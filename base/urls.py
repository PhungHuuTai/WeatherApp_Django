from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('load_more/<str:city>/<int:days>/', views.load_more_forecast, name='load_more_forecast'),
    path('weather_by_location/', views.weather_by_location, name='weather_by_location'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('confirm/<str:confirmation_code>/', views.confirm_subscription, name='confirm_subscription'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
]