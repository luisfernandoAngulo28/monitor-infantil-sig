"""
Servicios de análisis geoespacial y tracking
"""
from django.contrib.gis.geos import Point
from django.utils import timezone
from .models import PosicionGPS, Nino


class TrackingService:
    """
    Servicio para gestionar el tracking GPS de niños
    """
    
    @staticmethod
    def registrar_posicion(nino_id, latitud, longitud, **kwargs):
        """
        Registra una nueva posición GPS del niño
        
        Args:
            nino_id: ID del niño
            latitud: Coordenada latitud
            longitud: Coordenada longitud
            **kwargs: precision_metros, altitud, velocidad_kmh, nivel_bateria
        
        Returns:
            PosicionGPS creada
        """
        nino = Nino.objects.get(id=nino_id)
        
        # Crear punto GPS
        punto = Point(longitud, latitud, srid=4326)
        
        # Crear registro de posición
        posicion = PosicionGPS.objects.create(
            nino=nino,
            ubicacion=punto,
            precision_metros=kwargs.get('precision_metros'),
            altitud=kwargs.get('altitud'),
            velocidad_kmh=kwargs.get('velocidad_kmh'),
            nivel_bateria=kwargs.get('nivel_bateria'),
        )
        
        return posicion
    
    @staticmethod
    def obtener_ultima_posicion(nino_id):
        """Obtiene la última posición registrada del niño"""
        return PosicionGPS.objects.filter(
            nino_id=nino_id
        ).order_by('-timestamp').first()
    
    @staticmethod
    def obtener_historial_posiciones(nino_id, fecha_inicio=None, fecha_fin=None):
        """
        Obtiene el historial de posiciones de un niño
        """
        queryset = PosicionGPS.objects.filter(nino_id=nino_id)
        
        if fecha_inicio:
            queryset = queryset.filter(timestamp__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(timestamp__lte=fecha_fin)
        
        return queryset.order_by('-timestamp')
    
    @staticmethod
    def verificar_estado_nino(nino_id):
        """
        Verifica el estado actual del niño (dentro/fuera del área)
        """
        ultima_posicion = TrackingService.obtener_ultima_posicion(nino_id)
        
        if not ultima_posicion:
            return {
                'tiene_posicion': False,
                'dentro_area': None,
                'mensaje': 'No hay posiciones registradas'
            }
        
        # Verificar si la última posición es reciente (últimos 5 minutos)
        tiempo_transcurrido = timezone.now() - ultima_posicion.timestamp
        posicion_reciente = tiempo_transcurrido.total_seconds() < 300
        
        return {
            'tiene_posicion': True,
            'dentro_area': ultima_posicion.dentro_area_segura,
            'posicion_reciente': posicion_reciente,
            'ultima_actualizacion': ultima_posicion.timestamp,
            'latitud': ultima_posicion.ubicacion.y,
            'longitud': ultima_posicion.ubicacion.x,
            'nivel_bateria': ultima_posicion.nivel_bateria,
        }


class AnalisisSpatial:
    """
    Servicios de análisis espacial avanzado
    """
    
    @staticmethod
    def calcular_ruta_movimiento(nino_id, fecha_inicio, fecha_fin):
        """
        Genera una LineString con la ruta de movimiento del niño
        """
        from django.contrib.gis.geos import LineString
        
        posiciones = PosicionGPS.objects.filter(
            nino_id=nino_id,
            timestamp__gte=fecha_inicio,
            timestamp__lte=fecha_fin
        ).order_by('timestamp')
        
        if posiciones.count() < 2:
            return None
        
        puntos = [pos.ubicacion for pos in posiciones]
        return LineString(puntos, srid=4326)
    
    @staticmethod
    def detectar_puntos_salida(nino_id, fecha_inicio=None, fecha_fin=None):
        """
        Detecta todos los puntos donde el niño salió del área segura
        """
        queryset = PosicionGPS.objects.filter(
            nino_id=nino_id,
            dentro_area_segura=False
        )
        
        if fecha_inicio:
            queryset = queryset.filter(timestamp__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(timestamp__lte=fecha_fin)
        
        return queryset.order_by('timestamp')
