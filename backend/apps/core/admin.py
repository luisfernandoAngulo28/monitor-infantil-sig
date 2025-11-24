from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Tutor


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'tipo_usuario', 'is_active']
    list_filter = ['tipo_usuario', 'is_active', 'is_staff']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('tipo_usuario', 'telefono', 'direccion', 'foto_perfil', 
                      'firebase_token', 'notificaciones_activas')
        }),
    )


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'relacion', 'ci', 'telefono_emergencia', 'activo']
    list_filter = ['relacion', 'activo']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'ci']
