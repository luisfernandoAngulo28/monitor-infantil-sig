from django.contrib.gis import admin
from .models import CentroEducativo, Nino, PosicionGPS


@admin.register(CentroEducativo)
class CentroEducativoAdmin(admin.GISModelAdmin):
    """Admin con mapa interactivo para dibujar polígonos"""
    list_display = ['nombre', 'codigo', 'direccion', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']
    
    # Configuración del mapa en admin
    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 15,
            'default_lon': -63.1812,  # Santa Cruz, Bolivia
            'default_lat': -17.7833,
        },
    }


@admin.register(Nino)
class NinoAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'edad', 'centro_educativo', 
                    'tutor_principal', 'tracking_activo', 'activo']
    list_filter = ['sexo', 'centro_educativo', 'tracking_activo', 'activo']
    search_fields = ['nombre', 'apellido_paterno', 'apellido_materno']
    
    filter_horizontal = ['tutores_adicionales']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido_paterno', 'apellido_materno', 
                      'fecha_nacimiento', 'sexo', 'foto')
        }),
        ('Centro Educativo y Tutores', {
            'fields': ('centro_educativo', 'tutor_principal', 'tutores_adicionales')
        }),
        ('Configuración de Tracking', {
            'fields': ('dispositivo_id', 'tracking_activo', 'activo')
        }),
    )


@admin.register(PosicionGPS)
class PosicionGPSAdmin(admin.GISModelAdmin):
    """Admin con mapa para visualizar posiciones GPS"""
    list_display = ['nino', 'timestamp', 'dentro_area_segura', 
                    'precision_metros', 'nivel_bateria']
    list_filter = ['dentro_area_segura', 'timestamp']
    search_fields = ['nino__nombre', 'nino__apellido_paterno']
    readonly_fields = ['timestamp', 'dentro_area_segura']
    
    date_hierarchy = 'timestamp'
    
    # Mostrar las últimas 100 posiciones por defecto
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('nino', 'nino__centro_educativo')[:100]
