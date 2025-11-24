from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ninos_list(request):
    """Lista de niños de prueba"""
    return JsonResponse({
        'results': [
            {
                'id': 1,
                'nombre': 'Juan Pérez',
                'edad': 8,
                'ultima_ubicacion': {
                    'latitud': 19.4326,
                    'longitud': -99.1332,
                    'timestamp': '2024-11-23T10:30:00Z'
                },
                'estado_alerta': 'SEGURO'
            },
            {
                'id': 2,
                'nombre': 'María González',
                'edad': 7,
                'ultima_ubicacion': {
                    'latitud': 19.4340,
                    'longitud': -99.1350,
                    'timestamp': '2024-11-23T10:28:00Z'
                },
                'estado_alerta': 'SEGURO'
            }
        ]
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fcm_token_update(request):
    """Recibe token FCM"""
    token = request.data.get('firebase_token')
    print(f"✅ FCM Token recibido: {token}")
    return JsonResponse({'status': 'success', 'message': 'Token guardado'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_ninos(request):
    """Lista de niños del tutor"""
    return JsonResponse([
        {
            'id': 1,
            'nombre': 'Juan',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'López',
            'nombre_completo': 'Juan Pérez López',
            'fecha_nacimiento': '2016-03-15',
            'edad': 8,
            'sexo': 'M',
            'foto': None,
            'centro_educativo': {
                'id': 1,
                'nombre': 'Escuela Primaria Benito Juárez',
                'codigo': 'EPB001',
                'direccion': 'Av. Insurgentes 123, CDMX',
                'telefono': '5555551234'
            },
            'tracking_activo': True,
            'activo': True
        },
        {
            'id': 2,
            'nombre': 'María',
            'apellido_paterno': 'González',
            'apellido_materno': 'Ramírez',
            'nombre_completo': 'María González Ramírez',
            'fecha_nacimiento': '2017-08-22',
            'edad': 7,
            'sexo': 'F',
            'foto': None,
            'centro_educativo': {
                'id': 1,
                'nombre': 'Escuela Primaria Benito Juárez',
                'codigo': 'EPB001',
                'direccion': 'Av. Insurgentes 123, CDMX',
                'telefono': '5555551234'
            },
            'tracking_activo': True,
            'activo': True
        }
    ], safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estado_nino(request, nino_id):
    """Estado actual de un niño"""
    nombres = {1: 'Juan Pérez López', 2: 'María González Ramírez'}
    return JsonResponse({
        'nino': {
            'id': nino_id,
            'nombre_completo': nombres.get(nino_id, 'Desconocido')
        },
        'ultima_posicion': {
            'latitud': 19.4326 + (nino_id * 0.001),
            'longitud': -99.1332 + (nino_id * 0.001),
            'timestamp': '2024-11-24T09:00:00Z',
            'precision': 10.5
        },
        'dentro_area_segura': True,
        'alertas_activas': 0,
        'nivel_bateria': 85
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_alertas(request):
    """Lista de alertas del tutor"""
    return JsonResponse([], safe=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/ninos/', ninos_list, name='ninos-list'),
    path('api/ninos/<int:nino_id>/estado/', estado_nino, name='estado-nino'),
    path('api/configuracion/actualizar_firebase_token/', fcm_token_update, name='fcm-token'),
    path('api/configuracion/mis_ninos/', mis_ninos, name='mis-ninos'),
    path('api/mis-alertas/', mis_alertas, name='mis-alertas'),
]
