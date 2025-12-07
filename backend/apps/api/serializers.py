"""
Serializers para la API REST
"""
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from apps.gis_tracking.models import CentroEducativo, Nino, PosicionGPS
from apps.alerts.models import Alerta, NotificacionTutor
from apps.core.models import Tutor, Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'tipo_usuario', 'telefono', 'notificaciones_activas']
        read_only_fields = ['id']


class TutorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Tutor
        fields = ['id', 'usuario', 'relacion', 'ci', 'telefono_emergencia', 'activo']


class CentroEducativoSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple para CentroEducativo (sin campos geo)"""
    
    class Meta:
        model = CentroEducativo
        fields = ['id', 'nombre', 'codigo', 'direccion', 'telefono', 'activo']


class CentroEducativoSerializer(GeoFeatureModelSerializer):
    """Serializer con soporte geoespacial para CentroEducativo"""
    
    class Meta:
        model = CentroEducativo
        geo_field = 'area_segura'
        fields = ['id', 'nombre', 'codigo', 'direccion', 'telefono', 
                 'ubicacion_centro', 'margen_metros', 'activo']


class NinoSerializer(serializers.ModelSerializer):
    centro_educativo = CentroEducativoSimpleSerializer(read_only=True)
    tutor_principal = TutorSerializer(read_only=True)
    edad = serializers.IntegerField(read_only=True)
    nombre_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Nino
        fields = ['id', 'nombre', 'apellido_paterno', 'apellido_materno',
                 'nombre_completo', 'fecha_nacimiento', 'edad', 'sexo', 'foto',
                 'centro_educativo', 'tutor_principal', 'dispositivo_id',
                 'tracking_activo', 'activo']


class PosicionGPSSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple para PosicionGPS (sin campos geo)"""
    nino_nombre = serializers.CharField(source='nino.nombre_completo', read_only=True)
    latitud = serializers.SerializerMethodField()
    longitud = serializers.SerializerMethodField()
    distancia_centro = serializers.SerializerMethodField()
    
    class Meta:
        model = PosicionGPS
        fields = ['id', 'nino', 'nino_nombre', 'timestamp', 'dentro_area_segura',
                 'precision_metros', 'altitud', 'velocidad_kmh', 'nivel_bateria',
                 'latitud', 'longitud', 'distancia_centro']
        read_only_fields = ['dentro_area_segura']
    
    def get_latitud(self, obj):
        return obj.ubicacion.y if obj.ubicacion else None
    
    def get_longitud(self, obj):
        return obj.ubicacion.x if obj.ubicacion else None
    
    def get_distancia_centro(self, obj):
        return obj.distancia_al_centro()


class PosicionGPSSerializer(GeoFeatureModelSerializer):
    """Serializer con soporte geoespacial para PosicionGPS"""
    nino_nombre = serializers.CharField(source='nino.nombre_completo', read_only=True)
    distancia_centro = serializers.SerializerMethodField()
    
    class Meta:
        model = PosicionGPS
        geo_field = 'ubicacion'
        fields = ['id', 'nino', 'nino_nombre', 'timestamp', 'dentro_area_segura',
                 'precision_metros', 'altitud', 'velocidad_kmh', 'nivel_bateria',
                 'distancia_centro']
        read_only_fields = ['dentro_area_segura']
    
    def get_distancia_centro(self, obj):
        return obj.distancia_al_centro()


class RegistrarPosicionSerializer(serializers.Serializer):
    """Serializer para registrar una nueva posición GPS desde móvil"""
    nino_id = serializers.IntegerField()
    latitud = serializers.FloatField(min_value=-90, max_value=90)
    longitud = serializers.FloatField(min_value=-180, max_value=180)
    precision_metros = serializers.FloatField(required=False, allow_null=True)
    altitud = serializers.FloatField(required=False, allow_null=True)
    velocidad_kmh = serializers.FloatField(required=False, allow_null=True)
    nivel_bateria = serializers.IntegerField(
        required=False, 
        allow_null=True,
        min_value=0,
        max_value=100
    )


class AlertaSerializer(serializers.ModelSerializer):
    nino = NinoSerializer(read_only=True)
    posicion_gps = PosicionGPSSerializer(read_only=True)
    
    class Meta:
        model = Alerta
        fields = ['id', 'nino', 'tipo_alerta', 'estado', 'posicion_gps',
                 'fecha_creacion', 'fecha_enviada', 'fecha_leida', 'fecha_resuelta',
                 'mensaje']


class NotificacionTutorSerializer(serializers.ModelSerializer):
    alerta = AlertaSerializer(read_only=True)
    
    class Meta:
        model = NotificacionTutor
        fields = ['id', 'alerta', 'fecha_enviada', 'enviada_exitosamente', 
                 'fecha_leida', 'error_mensaje']


class EstadoNinoSerializer(serializers.Serializer):
    """Serializer para el estado actual de un niño"""
    nino = NinoSerializer()
    ultima_posicion = PosicionGPSSimpleSerializer(allow_null=True)
    dentro_area_segura = serializers.BooleanField()
    alertas_activas = serializers.IntegerField()
    nivel_bateria = serializers.IntegerField(allow_null=True)


class ActualizarFirebaseTokenSerializer(serializers.Serializer):
    """Serializer para actualizar el token FCM del usuario"""
    firebase_token = serializers.CharField(max_length=255)


class IngestaGPSChinoSerializer(serializers.Serializer):
    """Serializer para ingestar datos de GPS desde dispositivo chino GF21"""
    device_id = serializers.CharField(
        max_length=255,
        help_text='IMEI del dispositivo GPS'
    )
    lat = serializers.FloatField(
        min_value=-90,
        max_value=90,
        help_text='Latitud en grados decimales'
    )
    lon = serializers.FloatField(
        min_value=-180,
        max_value=180,
        help_text='Longitud en grados decimales'
    )
    satellites = serializers.IntegerField(
        min_value=0,
        max_value=50,
        required=False,
        default=0,
        help_text='Número de satélites GPS detectados'
    )
    battery = serializers.IntegerField(
        min_value=0,
        max_value=100,
        required=False,
        allow_null=True,
        help_text='Nivel de batería (0-100%)'
    )
    altitude = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text='Altitud en metros'
    )
    speed = serializers.FloatField(
        required=False,
        allow_null=True,
        help_text='Velocidad en km/h'
    )
