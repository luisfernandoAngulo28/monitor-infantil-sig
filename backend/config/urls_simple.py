from django.urls import path
from django.contrib import admin
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
            'nombre': 'Juan Pérez',
            'edad': 8,
            'foto': None,
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
            'foto': None,
            'ultima_ubicacion': {
                'latitud': 19.4340,
                'longitud': -99.1350,
                'timestamp': '2024-11-23T10:28:00Z'
            },
            'estado_alerta': 'SEGURO'
        }
    ], safe=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/ninos/', ninos_list, name='ninos-list'),
    path('api/configuracion/actualizar_firebase_token/', fcm_token_update, name='fcm-token'),
    path('api/configuracion/mis_ninos/', mis_ninos, name='mis-ninos'),
]
