# apps/alerts/notifications.py
"""
Sistema de Notificaciones Tipificadas para Monitor Infantil SIG
Inspirado en las mejores prácticas del clon de Uber/InDriver
"""

from firebase_admin import messaging
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class TipoAlerta:
    """Tipos de alertas con configuraciones específicas"""
    
    SALIDA_AREA = 'SALIDA_AREA'
    VELOCIDAD_ALTA = 'VELOCIDAD_ALTA'
    BATERIA_BAJA = 'BATERIA_BAJA'
    REGRESO_AREA = 'REGRESO_AREA'
    DISPOSITIVO_APAGADO = 'DISPOSITIVO_APAGADO'
    ENTRADA_KINDER = 'ENTRADA_KINDER'
    SALIDA_KINDER = 'SALIDA_KINDER'


class NotificationService:
    """
    Servicio de notificaciones mejorado con tipificación
    
    Características:
    - Notificaciones tipificadas con prioridades
    - Sonidos personalizados por tipo
    - Íconos y colores según criticidad
    - Soporte Android + iOS
    """
    
    # Configuraciones por tipo de alerta
    CONFIGURACIONES = {
        TipoAlerta.SALIDA_AREA: {
            'titulo': '🚨 Alerta de Seguridad',
            'icono': 'warning',
            'prioridad': 'high',
            'sonido': 'alarma',
            'color': '#FF0000',  # Rojo
            'vibration': [0, 500, 200, 500],  # Patrón de vibración
            'channel_id': 'alertas_criticas',
        },
        TipoAlerta.VELOCIDAD_ALTA: {
            'titulo': '⚠️ Velocidad Anormal Detectada',
            'icono': 'speed',
            'prioridad': 'high',
            'sonido': 'alerta',
            'color': '#FF6600',  # Naranja
            'vibration': [0, 300, 200, 300],
            'channel_id': 'alertas_criticas',
        },
        TipoAlerta.BATERIA_BAJA: {
            'titulo': '🔋 Batería Baja',
            'icono': 'battery_alert',
            'prioridad': 'normal',
            'sonido': 'default',
            'color': '#FFA500',  # Amarillo/Naranja
            'vibration': [0, 200],
            'channel_id': 'alertas_informativas',
        },
        TipoAlerta.REGRESO_AREA: {
            'titulo': '✅ Regresó al Área Segura',
            'icono': 'check_circle',
            'prioridad': 'normal',
            'sonido': 'success',
            'color': '#00C853',  # Verde
            'vibration': [0, 100],
            'channel_id': 'alertas_informativas',
        },
        TipoAlerta.DISPOSITIVO_APAGADO: {
            'titulo': '📵 Dispositivo Sin Señal',
            'icono': 'phonelink_off',
            'prioridad': 'high',
            'sonido': 'alerta',
            'color': '#9E9E9E',  # Gris
            'vibration': [0, 400, 200, 400],
            'channel_id': 'alertas_criticas',
        },
        TipoAlerta.ENTRADA_KINDER: {
            'titulo': '🏫 Llegó al Kinder',
            'icono': 'school',
            'prioridad': 'normal',
            'sonido': 'notification',
            'color': '#2196F3',  # Azul
            'vibration': [0, 150],
            'channel_id': 'alertas_informativas',
        },
        TipoAlerta.SALIDA_KINDER: {
            'titulo': '🚪 Salió del Kinder',
            'icono': 'exit_to_app',
            'prioridad': 'high',
            'sonido': 'alerta',
            'color': '#FF9800',  # Naranja
            'vibration': [0, 300, 150, 300],
            'channel_id': 'alertas_criticas',
        },
    }
    
    @classmethod
    def enviar_notificacion(
        cls,
        fcm_token: str,
        tipo: str,
        nino_nombre: str,
        mensaje_extra: str = '',
        data: Optional[Dict[str, Any]] = None,
        imagen_url: Optional[str] = None
    ) -> bool:
        """
        Enviar notificación push tipificada
        
        Args:
            fcm_token: Token FCM del dispositivo
            tipo: Tipo de alerta (usar TipoAlerta.*)
            nino_nombre: Nombre del niño
            mensaje_extra: Información adicional
            data: Datos extra para la app
            imagen_url: URL de imagen (opcional)
            
        Returns:
            bool: True si se envió correctamente
        """
        try:
            # Obtener configuración del tipo de alerta
            config = cls.CONFIGURACIONES.get(
                tipo,
                cls.CONFIGURACIONES[TipoAlerta.SALIDA_AREA]  # Default
            )
            
            # Construir mensaje completo
            if mensaje_extra:
                mensaje_completo = f"{nino_nombre} - {mensaje_extra}"
            else:
                mensaje_completo = nino_nombre
            
            # Preparar datos adicionales
            notification_data = data or {}
            notification_data.update({
                'tipo_alerta': tipo,
                'nino': nino_nombre,
                'timestamp': str(messaging.time.time()),
                'click_action': 'FLUTTER_NOTIFICATION_CLICK',
            })
            
            # Construir notificación base
            notification = messaging.Notification(
                title=config['titulo'],
                body=mensaje_completo,
                image=imagen_url,
            )
            
            # Configuración específica de Android
            android_config = messaging.AndroidConfig(
                priority=config['prioridad'],
                notification=messaging.AndroidNotification(
                    icon=config['icono'],
                    sound=f"{config['sonido']}.mp3",
                    channel_id=config['channel_id'],
                    color=config['color'],
                    tag=tipo,  # Agrupa notificaciones del mismo tipo
                    vibrate_timings_millis=config['vibration'],
                    notification_priority=messaging.Priority.HIGH 
                        if config['prioridad'] == 'high' 
                        else messaging.Priority.DEFAULT,
                ),
                ttl=3600,  # Time to live: 1 hora
            )
            
            # Configuración específica de iOS (APNS)
            apns_config = messaging.APNSConfig(
                headers={
                    'apns-priority': '10' if config['prioridad'] == 'high' else '5',
                },
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        alert=messaging.ApsAlert(
                            title=config['titulo'],
                            body=mensaje_completo,
                        ),
                        badge=1,
                        sound=f"{config['sonido']}.aiff",
                        category=tipo,
                        thread_id=f"nino_{nino_nombre}",  # Agrupa por niño
                    ),
                ),
            )
            
            # Crear mensaje completo
            message = messaging.Message(
                notification=notification,
                data=notification_data,
                android=android_config,
                apns=apns_config,
                token=fcm_token,
            )
            
            # Enviar notificación
            response = messaging.send(message)
            logger.info(
                f'✅ Notificación enviada exitosamente: {tipo} → {nino_nombre}'
                f' | Response: {response}'
            )
            return True
            
        except messaging.UnregisteredError:
            logger.error(f'❌ Token FCM no registrado o inválido: {fcm_token}')
            return False
            
        except Exception as e:
            logger.error(
                f'❌ Error enviando notificación {tipo}: {str(e)}',
                exc_info=True
            )
            return False
    
    @classmethod
    def enviar_notificacion_multiple(
        cls,
        fcm_tokens: list[str],
        tipo: str,
        nino_nombre: str,
        mensaje_extra: str = '',
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, int]:
        """
        Enviar notificación a múltiples dispositivos
        
        Args:
            fcm_tokens: Lista de tokens FCM
            tipo: Tipo de alerta
            nino_nombre: Nombre del niño
            mensaje_extra: Información adicional
            data: Datos extra
            
        Returns:
            dict: {'exitosos': int, 'fallidos': int}
        """
        exitosos = 0
        fallidos = 0
        
        for token in fcm_tokens:
            if cls.enviar_notificacion(
                fcm_token=token,
                tipo=tipo,
                nino_nombre=nino_nombre,
                mensaje_extra=mensaje_extra,
                data=data
            ):
                exitosos += 1
            else:
                fallidos += 1
        
        logger.info(
            f'📊 Notificaciones enviadas: '
            f'{exitosos} exitosas, {fallidos} fallidas'
        )
        
        return {'exitosos': exitosos, 'fallidos': fallidos}
    
    @classmethod
    def notificar_salida_area(
        cls,
        fcm_token: str,
        nino_nombre: str,
        kinder_nombre: str,
        distancia_metros: float,
        ubicacion_actual: str
    ) -> bool:
        """Notificación específica: niño salió del área segura"""
        return cls.enviar_notificacion(
            fcm_token=fcm_token,
            tipo=TipoAlerta.SALIDA_AREA,
            nino_nombre=nino_nombre,
            mensaje_extra=f"salió de {kinder_nombre} ({distancia_metros:.0f}m)",
            data={
                'kinder': kinder_nombre,
                'distancia': str(distancia_metros),
                'ubicacion': ubicacion_actual,
            }
        )
    
    @classmethod
    def notificar_velocidad_alta(
        cls,
        fcm_token: str,
        nino_nombre: str,
        velocidad_kmh: float
    ) -> bool:
        """Notificación específica: velocidad anormal detectada"""
        return cls.enviar_notificacion(
            fcm_token=fcm_token,
            tipo=TipoAlerta.VELOCIDAD_ALTA,
            nino_nombre=nino_nombre,
            mensaje_extra=f"se mueve a {velocidad_kmh:.0f} km/h (posible vehículo)",
            data={'velocidad': str(velocidad_kmh)}
        )
    
    @classmethod
    def notificar_bateria_baja(
        cls,
        fcm_token: str,
        nino_nombre: str,
        nivel_bateria: int
    ) -> bool:
        """Notificación específica: batería baja"""
        return cls.enviar_notificacion(
            fcm_token=fcm_token,
            tipo=TipoAlerta.BATERIA_BAJA,
            nino_nombre=nino_nombre,
            mensaje_extra=f"batería al {nivel_bateria}%",
            data={'bateria': str(nivel_bateria)}
        )
    
    @classmethod
    def notificar_regreso_area(
        cls,
        fcm_token: str,
        nino_nombre: str,
        kinder_nombre: str
    ) -> bool:
        """Notificación específica: niño regresó al área segura"""
        return cls.enviar_notificacion(
            fcm_token=fcm_token,
            tipo=TipoAlerta.REGRESO_AREA,
            nino_nombre=nino_nombre,
            mensaje_extra=f"regresó a {kinder_nombre}",
            data={'kinder': kinder_nombre}
        )


# ===================================================================
# EJEMPLO DE USO
# ===================================================================

"""
# En el modelo PosicionGPS al detectar salida del área:

from apps.alerts.notifications import NotificationService, TipoAlerta

def save(self, *args, **kwargs):
    if not self.dentro_area_segura and self.nino.tutor.fcm_token:
        # Notificar salida del área
        NotificationService.notificar_salida_area(
            fcm_token=self.nino.tutor.fcm_token,
            nino_nombre=self.nino.nombre_completo,
            kinder_nombre=self.nino.centro_educativo.nombre,
            distancia_metros=self.distancia_centro or 0,
            ubicacion_actual=f"{self.ubicacion.y}, {self.ubicacion.x}"
        )
    
    # Si detecta velocidad alta
    if self.velocidad and self.velocidad > 50:
        NotificationService.notificar_velocidad_alta(
            fcm_token=self.nino.tutor.fcm_token,
            nino_nombre=self.nino.nombre_completo,
            velocidad_kmh=self.velocidad
        )
    
    super().save(*args, **kwargs)
"""
