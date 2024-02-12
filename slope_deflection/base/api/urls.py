from django.urls import path
from .views import calculate_coordinates

urlpatterns = [
    path('calculate-coordinates/', calculate_coordinates, name='calculate_coordinates'),
]
