"""
Modelos de usuarios y roles del sistema
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuario extendido del sistema
    Puede ser: Tutor, Administrador del Kinder, etc.
    """
    TIPO_USUARIO = [
        ('TUTOR', 'Tutor/Madre/Padre'),
        ('ADMIN_KINDER', 'Administrador Kinder'),
        ('SUPERADMIN', 'Super Administrador'),
    ]
    
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO,
        default='TUTOR'
    )
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    foto_perfil = models.ImageField(
        upload_to='usuarios/perfiles/',
        blank=True,
        null=True
    )
    
    # Para notificaciones push
    firebase_token = models.CharField(
        max_length=255,
        blank=True,
        help_text='Token FCM para notificaciones push'
    )
    
    notificaciones_activas = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_tipo_usuario_display()})"


class Tutor(models.Model):
    """
    Tutor/Padre/Madre de un niño
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='tutor_profile'
    )
    
    TIPO_RELACION = [
        ('MADRE', 'Madre'),
        ('PADRE', 'Padre'),
        ('ABUELO', 'Abuelo/a'),
        ('TIO', 'Tío/a'),
        ('OTRO', 'Otro'),
    ]
    
    relacion = models.CharField(
        max_length=20,
        choices=TIPO_RELACION,
        default='MADRE'
    )
    
    ci = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Carnet de Identidad'
    )
    
    telefono_emergencia = models.CharField(max_length=20)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutores'
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_relacion_display()}"
