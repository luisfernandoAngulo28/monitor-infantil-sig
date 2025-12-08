"""
ViewSets y vistas de la API REST
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.contrib.gis.geos import Point
from datetime import timedelta

from apps.gis_tracking.models import CentroEducativo, Nino, PosicionGPS
from apps.gis_tracking.services import TrackingService
from apps.gis_tracking.traccar_service import TraccarService
from apps.alerts.models import Alerta, NotificacionTutor
from apps.core.models import Tutor
from django.conf import settings

from .serializers import (
    CentroEducativoSerializer, NinoSerializer, PosicionGPSSerializer,
    PosicionGPSSimpleSerializer, AlertaSerializer, NotificacionTutorSerializer, 
    TutorSerializer, RegistrarPosicionSerializer, EstadoNinoSerializer,
    ActualizarFirebaseTokenSerializer, IngestaGPSChinoSerializer,
    CrearNinoSerializer, ActualizarNinoSerializer, TraccarWebhookSerializer
)


class CentroEducativoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para consultar centros educativos
    GET /api/centros/ - Listar todos
    GET /api/centros/{id}/ - Detalle
    """
    queryset = CentroEducativo.objects.filter(activo=True)
    serializer_class = CentroEducativoSerializer
    permission_classes = [permissions.IsAuthenticated]


class NinoViewSet(viewsets.ModelViewSet):
    """
    API para gestionar niños (CRUD completo)
    GET /api/ninos/ - Listar
    GET /api/ninos/{id}/ - Detalle
    POST /api/ninos/ - Registrar nuevo niño
    PATCH /api/ninos/{id}/ - Actualizar niño
    DELETE /api/ninos/{id}/ - Eliminar niño (soft delete)
    GET /api/ninos/{id}/estado/ - Estado actual del niño
    GET /api/ninos/{id}/historial/ - Historial de posiciones
    POST /api/ninos/{id}/registrar_posicion/ - Registrar nueva posición GPS
    POST /api/ninos/{id}/desvincular_dispositivo/ - Desvincular dispositivo GPS
    """
    queryset = Nino.objects.filter(activo=True).select_related(
        'centro_educativo', 'tutor_principal'
    )
    serializer_class = NinoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Temporalmente permisivo para testing
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['centro_educativo', 'tutor_principal', 'tracking_activo']
    
    def get_serializer_class(self):
        """Usar diferentes serializers según la acción"""
        if self.action == 'create':
            return CrearNinoSerializer
        elif self.action in ['update', 'partial_update']:
            return ActualizarNinoSerializer
        return NinoSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create para logging detallado y respuesta completa"""
        print(f"🔍 DEBUG create() - Request data: {request.data}")
        print(f"🔍 DEBUG create() - User: {request.user}, Authenticated: {request.user.is_authenticated}")
        print(f"🔍 DEBUG create() - Headers: {dict(request.headers)}")
        
        # Crear con CrearNinoSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Responder con NinoSerializer completo
        instance = serializer.instance
        response_serializer = NinoSerializer(instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        """Filtrar niños del tutor autenticado"""
        user = self.request.user
        
        # Superusuarios ven todos
        if user.is_superuser:
            return Nino.objects.filter(activo=True)
        
        # Tutores ven solo sus niños
        try:
            tutor = Tutor.objects.get(usuario=user)
            from django.db.models import Q
            return Nino.objects.filter(
                Q(tutor_principal=tutor) | Q(tutores_adicionales=tutor),
                activo=True
            ).distinct()
        except Tutor.DoesNotExist:
            return Nino.objects.none()
    
    def perform_create(self, serializer):
        """Asignar tutor_principal al crear niño"""
        user = self.request.user
        print(f"🔍 DEBUG - Usuario autenticado: {user}, Is authenticated: {user.is_authenticated}")
        print(f"🔍 DEBUG - Datos recibidos: {self.request.data}")
        
        if user.is_authenticated:
            try:
                tutor = Tutor.objects.get(usuario=user)
                print(f"🔍 DEBUG - Tutor encontrado: {tutor.id}")
                serializer.save(tutor_principal=tutor)
                return
            except Tutor.DoesNotExist:
                print(f"❌ DEBUG - Tutor no existe para usuario: {user.username}")
        
        # Si no está autenticado o no tiene tutor, usar el primer tutor disponible (SOLO PARA TESTING)
        print(f"⚠️ DEBUG - Usando tutor por defecto para testing")
        tutor_default = Tutor.objects.first()
        if tutor_default:
            serializer.save(tutor_principal=tutor_default)
        else:
            raise permissions.PermissionDenied("No hay tutores disponibles en el sistema")
    
    def perform_destroy(self, instance):
        """Soft delete - marcar como inactivo"""
        instance.activo = False
        instance.tracking_activo = False
        instance.save()
        
        # Si tiene dispositivo, eliminarlo de Traccar
        if instance.dispositivo_id:
            try:
                traccar = TraccarService()
                traccar.delete_device(instance.dispositivo_id)
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Error al eliminar dispositivo de Traccar: {e}")
    
    @action(detail=True, methods=['get'])
    def estado(self, request, pk=None):
        """
        Obtiene el estado actual del niño
        GET /api/ninos/{id}/estado/
        """
        nino = self.get_object()
        estado_info = TrackingService.verificar_estado_nino(nino.id)
        
        ultima_pos = TrackingService.obtener_ultima_posicion(nino.id)
        alertas_activas = Alerta.objects.filter(
            nino=nino,
            estado__in=['PENDIENTE', 'ENVIADA']
        ).count()
        
        data = {
            'nino': NinoSerializer(nino).data,
            'ultima_posicion': PosicionGPSSimpleSerializer(ultima_pos).data if ultima_pos else None,
            'dentro_area_segura': estado_info.get('dentro_area', None),
            'alertas_activas': alertas_activas,
            'nivel_bateria': estado_info.get('nivel_bateria'),
            'tracking_activo': nino.tracking_activo,
        }
        
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def historial(self, request, pk=None):
        """
        Obtiene historial de posiciones del niño
        GET /api/ninos/{id}/historial/?dias=1
        """
        nino = self.get_object()
        
        # Parámetro de días (por defecto 1 día)
        dias = int(request.query_params.get('dias', 1))
        fecha_inicio = timezone.now() - timedelta(days=dias)
        
        posiciones = TrackingService.obtener_historial_posiciones(
            nino.id,
            fecha_inicio=fecha_inicio
        )
        
        serializer = PosicionGPSSerializer(posiciones, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def registrar_posicion(self, request, pk=None):
        """
        Registra una nueva posición GPS del niño
        POST /api/ninos/{id}/registrar_posicion/
        Body: {
            "latitud": -17.7833,
            "longitud": -63.1812,
            "precision_metros": 10.5,
            "nivel_bateria": 85
        }
        """
        nino = self.get_object()
        
        serializer = RegistrarPosicionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            posicion = TrackingService.registrar_posicion(
                nino_id=nino.id,
                latitud=serializer.validated_data['latitud'],
                longitud=serializer.validated_data['longitud'],
                precision_metros=serializer.validated_data.get('precision_metros'),
                altitud=serializer.validated_data.get('altitud'),
                velocidad_kmh=serializer.validated_data.get('velocidad_kmh'),
                nivel_bateria=serializer.validated_data.get('nivel_bateria'),
            )
            
            return Response(
                PosicionGPSSerializer(posicion).data,
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def desvincular_dispositivo(self, request, pk=None):
        """
        Desvincular dispositivo GPS del niño
        POST /api/ninos/{id}/desvincular_dispositivo/
        """
        nino = self.get_object()
        
        if not nino.dispositivo_id:
            return Response(
                {'mensaje': 'Este niño no tiene dispositivo vinculado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_device_id = nino.dispositivo_id
        
        # Eliminar de Traccar
        try:
            traccar = TraccarService()
            traccar.delete_device(old_device_id)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Error al eliminar de Traccar: {e}")
        
        # Limpiar dispositivo_id
        nino.dispositivo_id = None
        nino.tracking_activo = False
        nino.save()
        
        return Response(
            {
                'mensaje': f'Dispositivo {old_device_id} desvinculado exitosamente',
                'nino': NinoSerializer(nino).data
            },
            status=status.HTTP_200_OK
        )


class PosicionGPSViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para consultar posiciones GPS
    GET /api/posiciones/ - Listar posiciones recientes
    GET /api/posiciones/{id}/ - Detalle
    """
    queryset = PosicionGPS.objects.select_related('nino').order_by('-timestamp')[:100]
    serializer_class = PosicionGPSSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nino', 'dentro_area_segura']


class AlertaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar alertas
    GET /api/alertas/ - Listar alertas
    GET /api/alertas/{id}/ - Detalle
    PATCH /api/alertas/{id}/ - Actualizar estado
    POST /api/alertas/{id}/marcar_leida/ - Marcar como leída
    POST /api/alertas/{id}/resolver/ - Resolver alerta
    """
    queryset = Alerta.objects.select_related('nino', 'posicion_gps').order_by('-fecha_creacion')
    serializer_class = AlertaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nino', 'tipo_alerta', 'estado']
    
    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        """
        Marca una alerta como leída
        POST /api/alertas/{id}/marcar_leida/
        """
        alerta = self.get_object()
        alerta.marcar_como_leida()
        
        return Response(
            AlertaSerializer(alerta).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        """
        Resuelve una alerta
        POST /api/alertas/{id}/resolver/
        """
        alerta = self.get_object()
        alerta.resolver()
        
        return Response(
            AlertaSerializer(alerta).data,
            status=status.HTTP_200_OK
        )


class MisAlertasViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para que los tutores vean sus alertas
    GET /api/mis-alertas/ - Alertas del tutor autenticado
    """
    serializer_class = AlertaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtra alertas según el tutor autenticado"""
        user = self.request.user
        
        try:
            tutor = Tutor.objects.get(usuario=user)
            # Alertas de niños donde es tutor principal o adicional
            ninos_ids = list(tutor.ninos_principal.values_list('id', flat=True))
            ninos_ids.extend(tutor.ninos_adicional.values_list('id', flat=True))
            
            return Alerta.objects.filter(
                nino_id__in=ninos_ids
            ).order_by('-fecha_creacion')
        
        except Tutor.DoesNotExist:
            return Alerta.objects.none()


class ConfiguracionViewSet(viewsets.ViewSet):
    """
    API para configuración del usuario
    POST /api/configuracion/actualizar_firebase_token/ - Actualizar token FCM
    GET /api/configuracion/mis_ninos/ - Niños del tutor
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def actualizar_firebase_token(self, request):
        """
        Actualiza el token de Firebase del usuario
        POST /api/configuracion/actualizar_firebase_token/
        Body: {"firebase_token": "token..."}
        """
        serializer = ActualizarFirebaseTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        user.firebase_token = serializer.validated_data['firebase_token']
        user.save()
        
        return Response(
            {'mensaje': 'Token actualizado exitosamente'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def mis_ninos(self, request):
        """
        Obtiene los niños del tutor autenticado
        GET /api/configuracion/mis_ninos/
        """
        from django.db.models import Q
        user = request.user
        
        try:
            tutor = Tutor.objects.get(usuario=user)
            # Niños donde es tutor principal o adicional
            ninos = Nino.objects.filter(
                Q(tutor_principal=tutor) | Q(tutores_adicionales=tutor)
            ).distinct()
            
            serializer = NinoSerializer(ninos, many=True)
            return Response(serializer.data)
        
        except Tutor.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)


class BusquedaCercanosViewSet(viewsets.ViewSet):
    """ViewSet para búsquedas de ubicaciones cercanas"""
    pass


@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Permite acceso sin autenticación para dispositivos IoT
def ingesta_gps_chino(request):
    """
    Endpoint de ingesta para datos GPS desde dispositivos chinos (GF21)
    POST /api/ingesta/gps-chino/
    
    Payload esperado:
    {
        "device_id": "862104056214397",  # IMEI del GPS
        "lat": -17.7833,
        "lon": -63.1812,
        "satellites": 5,
        "battery": 85,
        "altitude": 420.5,  # Opcional
        "speed": 0.0        # Opcional
    }
    
    Lógica de Semáforo (Calidad de Señal):
    - satellites >= 3: Señal GPS fuerte → precisión = 10.0 metros
    - satellites < 3:  Señal LBS/Interior → precisión = 200.0 metros
    """
    serializer = IngestaGPSChinoSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {
                'error': 'Datos inválidos',
                'detalles': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    data = serializer.validated_data
    device_id = data['device_id']
    lat = data['lat']
    lon = data['lon']
    satellites = data.get('satellites', 0)
    battery = data.get('battery')
    altitude = data.get('altitude')
    speed = data.get('speed')
    
    # Buscar niño por dispositivo_id (IMEI)
    try:
        nino = Nino.objects.get(dispositivo_id=device_id, activo=True)
    except Nino.DoesNotExist:
        return Response(
            {
                'error': 'Dispositivo no encontrado',
                'mensaje': f'No existe ningún niño registrado con dispositivo_id: {device_id}'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verificar que el tracking esté activo
    if not nino.tracking_activo:
        return Response(
            {
                'error': 'Tracking desactivado',
                'mensaje': f'El tracking para {nino.nombre_completo()} está desactivado'
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    # LÓGICA DE SEMÁFORO: Calidad de señal GPS
    if satellites >= 3:
        # Señal GPS fuerte (3+ satélites)
        precision_metros = 10.0
    else:
        # Señal débil o LBS (< 3 satélites)
        precision_metros = 200.0
    
    # Crear punto geográfico (IMPORTANTE: PostGIS usa lon, lat)
    punto_gps = Point(lon, lat, srid=4326)
    
    # Crear registro de posición GPS
    posicion = PosicionGPS.objects.create(
        nino=nino,
        ubicacion=punto_gps,
        precision_metros=precision_metros,
        nivel_bateria=battery,
        altitud=altitude,
        velocidad_kmh=speed,
        timestamp=timezone.now()
    )
    
    # Serializar respuesta
    response_data = {
        'success': True,
        'mensaje': 'Posición GPS registrada exitosamente',
        'nino': {
            'id': nino.id,
            'nombre': nino.nombre_completo(),
            'centro_educativo': nino.centro_educativo.nombre
        },
        'posicion': {
            'id': posicion.id,
            'lat': lat,
            'lon': lon,
            'precision_metros': precision_metros,
            'satellites': satellites,
            'dentro_area_segura': posicion.dentro_area_segura,
            'timestamp': posicion.timestamp.isoformat()
        }
    }
    
    return Response(response_data, status=status.HTTP_201_CREATED)


class BusquedaCercanosViewSet(viewsets.ViewSet):
    """
    API para búsqueda espacial de niños cercanos
    GET /api/busqueda-cercanos/ninos-cercanos/{lat}/{lng}/?radius=1000
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'], url_path='ninos-cercanos/(?P<lat>[-\d.]+)/(?P<lng>[-\d.]+)')
    def ninos_cercanos(self, request, lat=None, lng=None):
        """
        Busca niños cercanos a una ubicación específica usando ST_Distance_Sphere
        
        Parámetros:
        - lat: Latitud del centro de búsqueda
        - lng: Longitud del centro de búsqueda  
        - radius: Radio de búsqueda en metros (query param, default 500m)
        
        Ejemplo:
        GET /api/busqueda-cercanos/ninos-cercanos/-17.7833/-63.1821/?radius=1000
        """
        from django.db import connection
        import re
        
        try:
            # Validar y convertir parámetros
            lat = float(lat)
            lng = float(lng)
            radius = int(request.query_params.get('radius', 500))
            
            # Validar rangos
            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                return Response(
                    {'error': 'Coordenadas inválidas'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if radius < 10 or radius > 50000:  # Entre 10m y 50km
                return Response(
                    {'error': 'Radio debe estar entre 10 y 50000 metros'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Query espacial con ST_Distance usando geography para metros
            query = """
                SELECT
                    n.id,
                    n.nombre,
                    n.apellido_paterno,
                    n.apellido_materno,
                    ST_AsText(p.ubicacion) AS ubicacion,
                    ST_Distance(
                        p.ubicacion::geography, 
                        ST_GeomFromText('POINT(%s %s)', 4326)::geography
                    ) AS distancia_metros,
                    p.timestamp,
                    p.dentro_area_segura,
                    p.velocidad_kmh,
                    p.precision_metros,
                    ce.nombre AS kinder_nombre,
                    ce.direccion AS kinder_direccion
                FROM
                    gis_tracking_nino n
                INNER JOIN
                    gis_tracking_posiciongps p ON n.id = p.nino_id
                INNER JOIN
                    gis_tracking_centroeducativo ce ON n.centro_educativo_id = ce.id
                WHERE
                    n.activo = TRUE
                    AND p.timestamp = (
                        SELECT MAX(timestamp) 
                        FROM gis_tracking_posiciongps 
                        WHERE nino_id = n.id
                    )
                    AND ST_Distance(
                        p.ubicacion::geography, 
                        ST_GeomFromText('POINT(%s %s)', 4326)::geography
                    ) <= %s
                ORDER BY
                    distancia_metros ASC
            """
            
            with connection.cursor() as cursor:
                cursor.execute(query, [lng, lat, lng, lat, radius])
                rows = cursor.fetchall()
            
            # Procesar resultados
            ninos_cercanos = []
            for row in rows:
                # Parsear geometría POINT(lng lat)
                position_text = row[4]
                match = re.match(r'POINT\(([-\d.]+) ([-\d.]+)\)', position_text)
                
                if match:
                    lng_nino = float(match.group(1))
                    lat_nino = float(match.group(2))
                    
                    # Construir nombre completo
                    apellido_completo = f"{row[2]} {row[3]}".strip() if row[3] else row[2]
                    
                    ninos_cercanos.append({
                        'id': row[0],
                        'nombre': row[1],
                        'apellido_paterno': row[2],
                        'apellido_materno': row[3] or '',
                        'nombre_completo': f"{row[1]} {apellido_completo}",
                        'posicion': {
                            'lat': lat_nino,
                            'lng': lng_nino
                        },
                        'distancia_metros': round(row[5], 2),
                        'distancia_km': round(row[5] / 1000, 3),
                        'ultima_actualizacion': row[6].isoformat() if row[6] else None,
                        'dentro_area_segura': row[7],
                        'velocidad_kmh': round(row[8], 1) if row[8] else 0,
                        'precision_metros': round(row[9], 1) if row[9] else None,
                        'kinder': {
                            'nombre': row[10],
                            'direccion': row[11]
                        },
                        'estado': '🟢 Seguro' if row[7] else '🔴 Fuera del área',
                        'estado_color': 'green' if row[7] else 'red'
                    })
            
            return Response({
                'centro_busqueda': {
                    'lat': lat,
                    'lng': lng
                },
                'radio_metros': radius,
                'total_encontrados': len(ninos_cercanos),
                'ninos': ninos_cercanos
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response(
                {'error': f'Parámetros inválidos: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error en la búsqueda: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def traccar_webhook(request):
    """
    Webhook endpoint para recibir actualizaciones de posición desde Traccar Server.
    POST /api/traccar/webhook/
    
    Traccar envía eventos de posición en tiempo real a este endpoint.
    
    Payload esperado:
    {
        "position": {
            "id": 12345,
            "deviceId": 1,
            "deviceTime": "2025-12-07T10:30:00.000Z",
            "latitude": -17.7833,
            "longitude": -63.1812,
            "speed": 0.0,
            "altitude": 420.5,
            "accuracy": 10.0,
            "attributes": {
                "batteryLevel": 85.0
            }
        },
        "device": {
            "id": 1,
            "uniqueId": "862104056214397",
            "name": "Juanito Pérez"
        }
    }
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Verificar token de autorización
    auth_header = request.headers.get('Authorization', '')
    expected_token = f"Bearer {settings.TRACCAR_WEBHOOK_SECRET}"
    
    if auth_header != expected_token:
        logger.warning(f"❌ Intento de acceso no autorizado al webhook Traccar")
        return Response(
            {'error': 'Unauthorized'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        serializer = TraccarWebhookSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"❌ Datos inválidos en webhook: {serializer.errors}")
            return Response(
                {'error': 'Invalid data', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        position_data = request.data.get('position')
        device_data = request.data.get('device')
        
        if not position_data or not device_data:
            return Response(
                {'error': 'Missing position or device data'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        device_id = device_data['uniqueId']
        
        # Buscar niño por dispositivo_id
        try:
            nino = Nino.objects.get(
                dispositivo_id=device_id,
                activo=True,
                tracking_activo=True
            )
        except Nino.DoesNotExist:
            logger.warning(f"⚠️ Dispositivo {device_id} no vinculado a ningún niño")
            return Response(
                {'error': f'No child registered with device ID: {device_id}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Usar TraccarService para sincronizar posición
        traccar = TraccarService()
        posicion = traccar.sync_position_to_django(nino, position_data)
        
        if posicion:
            logger.info(f"✅ Webhook procesado: {nino.nombre_completo()} - Posición ID {posicion.id}")
            return Response(
                {
                    'success': True,
                    'posicion_id': posicion.id,
                    'nino_id': nino.id,
                    'nino_nombre': nino.nombre_completo(),
                    'dentro_area_segura': posicion.dentro_area_segura,
                    'timestamp': posicion.timestamp.isoformat()
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'Failed to create position'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Exception as e:
        logger.error(f"❌ Error procesando webhook Traccar: {e}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
