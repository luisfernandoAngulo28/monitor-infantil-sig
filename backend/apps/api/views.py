"""
ViewSets y vistas de la API REST
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta

from apps.gis_tracking.models import CentroEducativo, Nino, PosicionGPS
from apps.gis_tracking.services import TrackingService
from apps.alerts.models import Alerta, NotificacionTutor
from apps.core.models import Tutor

from .serializers import (
    CentroEducativoSerializer, NinoSerializer, PosicionGPSSerializer,
    PosicionGPSSimpleSerializer, AlertaSerializer, NotificacionTutorSerializer, 
    TutorSerializer, RegistrarPosicionSerializer, EstadoNinoSerializer,
    ActualizarFirebaseTokenSerializer
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


class NinoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para consultar niños
    GET /api/ninos/ - Listar
    GET /api/ninos/{id}/ - Detalle
    GET /api/ninos/{id}/estado/ - Estado actual del niño
    GET /api/ninos/{id}/historial/ - Historial de posiciones
    POST /api/ninos/{id}/registrar_posicion/ - Registrar nueva posición GPS
    """
    queryset = Nino.objects.filter(activo=True).select_related(
        'centro_educativo', 'tutor_principal'
    )
    serializer_class = NinoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['centro_educativo', 'tutor_principal', 'tracking_activo']
    
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
        }
        
        serializer = EstadoNinoSerializer(data)
        return Response(serializer.data)
    
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
