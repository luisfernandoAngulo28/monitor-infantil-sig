from django.urls import path
from . import views

app_name = 'gis_tracking'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mapa/', views.mapa_tracking, name='mapa_tracking'),
]
