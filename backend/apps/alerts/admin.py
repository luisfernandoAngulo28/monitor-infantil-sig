from django.contrib import admin
from .models import Alerta, NotificacionTutor


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['nino', 'tipo_alerta', 'estado', 'fecha_creacion', 
                    'fecha_enviada', 'fecha_leida']
    list_filter = ['tipo_alerta', 'estado', 'fecha_creacion']
    search_fields = ['nino__nombre', 'nino__apellido_paterno', 'mensaje']
    readonly_fields = ['fecha_creacion', 'fecha_enviada', 'fecha_leida', 'fecha_resuelta']
    
    date_hierarchy = 'fecha_creacion'
    
    actions = ['marcar_como_resuelta']
    
    def marcar_como_resuelta(self, request, queryset):
        for alerta in queryset:
            alerta.resolver()
        self.message_user(request, f"{queryset.count()} alertas marcadas como resueltas")
    marcar_como_resuelta.short_description = "Marcar como resueltas"


@admin.register(NotificacionTutor)
class NotificacionTutorAdmin(admin.ModelAdmin):
    list_display = ['alerta', 'tutor', 'fecha_enviada', 'enviada_exitosamente', 'fecha_leida']
    list_filter = ['enviada_exitosamente', 'fecha_enviada']
    search_fields = ['tutor__usuario__first_name', 'tutor__usuario__last_name']
    readonly_fields = ['fecha_enviada', 'fecha_leida']
