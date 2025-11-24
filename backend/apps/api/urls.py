"""
URLs de la API REST
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    CentroEducativoViewSet,
    NinoViewSet,
    PosicionGPSViewSet,
    AlertaViewSet,
    MisAlertasViewSet,
    ConfiguracionViewSet,
)

app_name = 'api'

# Router para ViewSets
router = DefaultRouter()
router.register(r'centros', CentroEducativoViewSet, basename='centro')
router.register(r'ninos', NinoViewSet, basename='nino')
router.register(r'posiciones', PosicionGPSViewSet, basename='posicion')
router.register(r'alertas', AlertaViewSet, basename='alerta')
router.register(r'mis-alertas', MisAlertasViewSet, basename='mis-alertas')
router.register(r'configuracion', ConfiguracionViewSet, basename='configuracion')

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('', include(router.urls)),
]
