from django.urls import path
from .views import save_thresholds, get_thresholds  # ton POST + ce GET

urlpatterns = [
    path('save-thresholds/', save_thresholds, name='save_thresholds'),
    path('get-thresholds/', get_thresholds, name='get_thresholds'),
]
