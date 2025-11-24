from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import CentroEducativo, Nino, PosicionGPS
from apps.alerts.models import Alerta


@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    # Estadísticas
    total_ninos = Nino.objects.filter(activo=True).count()
    total_centros = CentroEducativo.objects.filter(activo=True).count()
    
    # Contar niños dentro del área (última posición)
    dentro_area = 0
    for nino in Nino.objects.filter(activo=True):
        ultima_pos = PosicionGPS.objects.filter(nino=nino).order_by('-timestamp').first()
        if ultima_pos and ultima_pos.dentro_area_segura:
            dentro_area += 1
    
    # Alertas activas
    alertas_activas = Alerta.objects.filter(
        estado__in=['PENDIENTE', 'ENVIADA']
    ).count()
    
    # Alertas recientes (últimas 5)
    alertas_recientes = Alerta.objects.select_related(
        'nino', 'posicion_gps'
    ).order_by('-fecha_creacion')[:5]
    
    context = {
        'total_ninos': total_ninos,
        'total_centros': total_centros,
        'dentro_area': dentro_area,
        'alertas_activas': alertas_activas,
        'alertas_recientes': alertas_recientes,
    }
    
    return render(request, 'gis_tracking/dashboard.html', context)


@login_required
def mapa_tracking(request):
    """Vista del mapa de tracking en tiempo real"""
    return render(request, 'gis_tracking/mapa.html')
