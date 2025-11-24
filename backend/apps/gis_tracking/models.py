"""
Modelos geoespaciales para tracking y monitoreo
"""
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils import timezone
from apps.core.models import Tutor


class CentroEducativo(models.Model):
    """
    Centro educativo/Kinder con área geográfica definida
    """
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(
        max_length=50,
        unique=True,
        help_text='Código único del centro educativo'
    )
    
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Campo geoespacial: Polígono del área del kinder
    area_segura = gis_models.PolygonField(
        srid=4326,
        help_text='Polígono que delimita el área segura del kinder'
    )
    
    # Punto central (calculado automáticamente)
    ubicacion_centro = gis_models.PointField(
        srid=4326,
        blank=True,
        null=True,
        help_text='Punto central del kinder (calculado del polígono)'
    )
    
    # Margen de tolerancia (opcional)
    margen_metros = models.IntegerField(
        default=0,
        help_text='Margen adicional en metros fuera del polígono (geofencing)'
    )
    
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Centro Educativo'
        verbose_name_plural = 'Centros Educativos'
        ordering = ['nombre']
    
    def save(self, *args, **kwargs):
        # Calcular el centroide del polígono automáticamente
        if self.area_segura and not self.ubicacion_centro:
            self.ubicacion_centro = self.area_segura.centroid
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class Nino(models.Model):
    """
    Niño/a que será monitoreado
    """
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True)
    
    fecha_nacimiento = models.DateField()
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    
    foto = models.ImageField(
        upload_to='ninos/fotos/',
        blank=True,
        null=True
    )
    
    # Relaciones
    centro_educativo = models.ForeignKey(
        CentroEducativo,
        on_delete=models.PROTECT,
        related_name='ninos'
    )
    
    tutor_principal = models.ForeignKey(
        Tutor,
        on_delete=models.PROTECT,
        related_name='ninos_principal'
    )
    
    tutores_adicionales = models.ManyToManyField(
        Tutor,
        blank=True,
        related_name='ninos_adicional',
        help_text='Tutores adicionales que reciben alertas'
    )
    
    # Información del dispositivo
    dispositivo_id = models.CharField(
        max_length=255,
        blank=True,
        help_text='ID del celular/smartwatch para tracking'
    )
    
    # Estado
    activo = models.BooleanField(default=True)
    tracking_activo = models.BooleanField(
        default=True,
        help_text='Si el tracking GPS está activo'
    )
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Niño/a'
        verbose_name_plural = 'Niños/as'
        ordering = ['apellido_paterno', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"
    
    def nombre_completo(self):
        if self.apellido_materno:
            return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
        return f"{self.nombre} {self.apellido_paterno}"
    
    @property
    def edad(self):
        """Calcula la edad actual del niño"""
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < 
            (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )


class PosicionGPS(models.Model):
    """
    Registro de posición GPS del niño en tiempo real
    """
    nino = models.ForeignKey(
        Nino,
        on_delete=models.CASCADE,
        related_name='posiciones'
    )
    
    # Campo geoespacial: Punto GPS
    ubicacion = gis_models.PointField(
        srid=4326,
        help_text='Coordenadas GPS (latitud, longitud)'
    )
    
    # Timestamp
    timestamp = models.DateTimeField(
        default=timezone.now,
        db_index=True
    )
    
    # Análisis espacial
    dentro_area_segura = models.BooleanField(
        default=True,
        help_text='¿El niño está dentro del área del kinder?'
    )
    
    # Metadatos GPS
    precision_metros = models.FloatField(
        null=True,
        blank=True,
        help_text='Precisión del GPS en metros'
    )
    
    altitud = models.FloatField(
        null=True,
        blank=True,
        help_text='Altitud en metros'
    )
    
    velocidad_kmh = models.FloatField(
        null=True,
        blank=True,
        help_text='Velocidad en km/h'
    )
    
    # Información del dispositivo
    nivel_bateria = models.IntegerField(
        null=True,
        blank=True,
        help_text='Nivel de batería del dispositivo (0-100)'
    )
    
    class Meta:
        verbose_name = 'Posición GPS'
        verbose_name_plural = 'Posiciones GPS'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['nino', '-timestamp']),
            models.Index(fields=['dentro_area_segura', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.nino} - {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}"
    
    def save(self, *args, **kwargs):
        """
        Análisis espacial automático: 
        Verificar si el punto está dentro del polígono del kinder
        """
        if self.ubicacion and self.nino.centro_educativo:
            area_kinder = self.nino.centro_educativo.area_segura
            
            # Análisis point-in-polygon con GeoDjango
            self.dentro_area_segura = area_kinder.contains(self.ubicacion)
            
            # Si hay margen de tolerancia, expandir el polígono
            if not self.dentro_area_segura and self.nino.centro_educativo.margen_metros > 0:
                # Buffer en metros (transformar a proyección métrica)
                area_con_margen = area_kinder.buffer(
                    self.nino.centro_educativo.margen_metros / 111320  # Aproximación a grados
                )
                self.dentro_area_segura = area_con_margen.contains(self.ubicacion)
        
        super().save(*args, **kwargs)
        
        # Trigger para crear alerta si salió del área
        if not self.dentro_area_segura:
            from apps.alerts.models import Alerta
            Alerta.crear_alerta_salida(self)
    
    def distancia_al_centro(self):
        """Calcula distancia en metros al centro del kinder"""
        if self.nino.centro_educativo.ubicacion_centro:
            from django.contrib.gis.measure import Distance
            return self.ubicacion.distance(
                self.nino.centro_educativo.ubicacion_centro
            ) * 111320  # Convertir grados a metros aproximadamente
        return None
