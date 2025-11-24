"""
Modelos para el sistema de alertas
"""
from django.db import models
from django.utils import timezone
from apps.gis_tracking.models import Nino, PosicionGPS
from apps.core.models import Tutor


class Alerta(models.Model):
    """
    Alerta generada cuando un niño sale del área segura
    """
    TIPO_ALERTA = [
        ('SALIDA_AREA', 'Salida del Área Segura'),
        ('BATERIA_BAJA', 'Batería Baja'),
        ('SIN_SEÑAL', 'Sin Señal GPS'),
        ('MANUAL', 'Alerta Manual'),
    ]
    
    ESTADO_ALERTA = [
        ('PENDIENTE', 'Pendiente'),
        ('ENVIADA', 'Enviada'),
        ('LEIDA', 'Leída'),
        ('RESUELTA', 'Resuelta'),
    ]
    
    nino = models.ForeignKey(
        Nino,
        on_delete=models.CASCADE,
        related_name='alertas'
    )
    
    tipo_alerta = models.CharField(
        max_length=20,
        choices=TIPO_ALERTA,
        default='SALIDA_AREA'
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_ALERTA,
        default='PENDIENTE'
    )
    
    # Posición GPS donde se generó la alerta
    posicion_gps = models.ForeignKey(
        PosicionGPS,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alertas_generadas'
    )
    
    # Timestamp
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_enviada = models.DateTimeField(null=True, blank=True)
    fecha_leida = models.DateTimeField(null=True, blank=True)
    fecha_resuelta = models.DateTimeField(null=True, blank=True)
    
    # Mensaje
    mensaje = models.TextField(blank=True)
    
    # Tutores notificados
    tutores_notificados = models.ManyToManyField(
        Tutor,
        through='NotificacionTutor',
        related_name='alertas_recibidas'
    )
    
    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['nino', '-fecha_creacion']),
            models.Index(fields=['estado', '-fecha_creacion']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_alerta_display()} - {self.nino} - {self.fecha_creacion}"
    
    @classmethod
    def crear_alerta_salida(cls, posicion_gps):
        """
        Crea una alerta cuando el niño sale del área
        Incluye cooldown para evitar spam de alertas
        """
        from datetime import timedelta
        
        # Verificar si ya existe una alerta reciente (últimos 5 minutos)
        tiempo_cooldown = timezone.now() - timedelta(minutes=5)
        alerta_reciente = cls.objects.filter(
            nino=posicion_gps.nino,
            tipo_alerta='SALIDA_AREA',
            fecha_creacion__gte=tiempo_cooldown,
            estado__in=['PENDIENTE', 'ENVIADA']
        ).exists()
        
        if alerta_reciente:
            return None  # No crear alerta duplicada
        
        # Crear nueva alerta
        mensaje = (
            f"⚠️ ALERTA: {posicion_gps.nino.nombre_completo()} ha salido del área segura "
            f"de {posicion_gps.nino.centro_educativo.nombre}. "
            f"Hora: {posicion_gps.timestamp.strftime('%H:%M:%S')}"
        )
        
        alerta = cls.objects.create(
            nino=posicion_gps.nino,
            tipo_alerta='SALIDA_AREA',
            posicion_gps=posicion_gps,
            mensaje=mensaje
        )
        
        # Enviar notificaciones a tutores
        alerta.enviar_notificaciones()
        
        return alerta
    
    def enviar_notificaciones(self):
        """
        Envía notificaciones push a todos los tutores
        """
        from .services import NotificacionService
        
        # Obtener todos los tutores (principal + adicionales)
        tutores = [self.nino.tutor_principal]
        tutores.extend(self.nino.tutores_adicionales.all())
        
        for tutor in tutores:
            NotificacionService.enviar_push_notification(
                tutor=tutor,
                alerta=self
            )
        
        self.estado = 'ENVIADA'
        self.fecha_enviada = timezone.now()
        self.save()
    
    def marcar_como_leida(self):
        """Marca la alerta como leída"""
        self.estado = 'LEIDA'
        self.fecha_leida = timezone.now()
        self.save()
    
    def resolver(self):
        """Marca la alerta como resuelta"""
        self.estado = 'RESUELTA'
        self.fecha_resuelta = timezone.now()
        self.save()


class NotificacionTutor(models.Model):
    """
    Registro de notificaciones enviadas a tutores
    """
    alerta = models.ForeignKey(
        Alerta,
        on_delete=models.CASCADE
    )
    
    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE
    )
    
    fecha_enviada = models.DateTimeField(auto_now_add=True)
    
    enviada_exitosamente = models.BooleanField(default=False)
    
    fecha_leida = models.DateTimeField(null=True, blank=True)
    
    # Metadatos
    mensaje_id = models.CharField(
        max_length=255,
        blank=True,
        help_text='ID del mensaje en Firebase/servicio push'
    )
    
    error_mensaje = models.TextField(
        blank=True,
        help_text='Mensaje de error si el envío falló'
    )
    
    class Meta:
        verbose_name = 'Notificación a Tutor'
        verbose_name_plural = 'Notificaciones a Tutores'
        ordering = ['-fecha_enviada']
    
    def __str__(self):
        return f"{self.alerta.tipo_alerta} -> {self.tutor.usuario.get_full_name()}"
