from django.urls import path
from .views import WeatherApp

urlpatterns = [
   
    path('', WeatherApp)
]
