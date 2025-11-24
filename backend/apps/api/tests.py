"""
Tests para la API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point, Polygon
from rest_framework.test import APIClient
from rest_framework import status

from apps.core.models import Usuario, Tutor
from apps.gis_tracking.models import CentroEducativo, Nino, PosicionGPS
from apps.alerts.models import Alerta

User = get_user_model()


class TrackingAPITestCase(TestCase):
    """Tests para el tracking GPS"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear usuario tutor
        self.usuario = Usuario.objects.create_user(
            username='tutor1',
            password='test123',
            first_name='María',
            last_name='González',
            tipo_usuario='TUTOR'
        )
        
        self.tutor = Tutor.objects.create(
            usuario=self.usuario,
            relacion='MADRE',
            ci='12345678',
            telefono_emergencia='70123456'
        )
        
        # Crear centro educativo con polígono
        poligono = Polygon((
            (-63.1820, -17.7840),
            (-63.1810, -17.7840),
            (-63.1810, -17.7830),
            (-63.1820, -17.7830),
            (-63.1820, -17.7840),
        ), srid=4326)
        
        self.kinder = CentroEducativo.objects.create(
            nombre='Kinder Los Pitufos',
            codigo='KP001',
            direccion='Av. San Martin #123',
            area_segura=poligono
        )
        
        # Crear niño
        from datetime import date
        self.nino = Nino.objects.create(
            nombre='Pedrito',
            apellido_paterno='González',
            fecha_nacimiento=date(2020, 5, 15),
            sexo='M',
            centro_educativo=self.kinder,
            tutor_principal=self.tutor,
            dispositivo_id='device123'
        )
        
        # Autenticar cliente
        self.client.force_authenticate(user=self.usuario)
    
    def test_registrar_posicion_dentro_area(self):
        """Test: Registrar posición dentro del área segura"""
        url = f'/api/ninos/{self.nino.id}/registrar_posicion/'
        data = {
            'latitud': -17.7835,  # Dentro del polígono
            'longitud': -63.1815,
            'nivel_bateria': 85
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['properties']['dentro_area_segura'])
        
        # Verificar que se creó la posición
        self.assertEqual(PosicionGPS.objects.count(), 1)
    
    def test_registrar_posicion_fuera_area(self):
        """Test: Registrar posición fuera del área - debe generar alerta"""
        url = f'/api/ninos/{self.nino.id}/registrar_posicion/'
        data = {
            'latitud': -17.7900,  # Fuera del polígono
            'longitud': -63.1900,
            'nivel_bateria': 80
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['properties']['dentro_area_segura'])
        
        # Verificar que se generó una alerta
        self.assertEqual(Alerta.objects.filter(tipo_alerta='SALIDA_AREA').count(), 1)
    
    def test_obtener_estado_nino(self):
        """Test: Obtener estado actual del niño"""
        # Crear una posición
        punto = Point(-63.1815, -17.7835, srid=4326)
        PosicionGPS.objects.create(
            nino=self.nino,
            ubicacion=punto,
            nivel_bateria=90
        )
        
        url = f'/api/ninos/{self.nino.id}/estado/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nino']['id'], self.nino.id)
        self.assertIsNotNone(response.data['ultima_posicion'])
        self.assertEqual(response.data['nivel_bateria'], 90)
    
    def test_historial_posiciones(self):
        """Test: Obtener historial de posiciones"""
        # Crear varias posiciones
        for i in range(5):
            punto = Point(-63.1815 + i*0.0001, -17.7835, srid=4326)
            PosicionGPS.objects.create(
                nino=self.nino,
                ubicacion=punto
            )
        
        url = f'/api/ninos/{self.nino.id}/historial/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 5)
    
    def test_mis_alertas(self):
        """Test: Tutor puede ver sus alertas"""
        # Crear alerta
        punto = Point(-63.1900, -17.7900, srid=4326)
        posicion = PosicionGPS.objects.create(
            nino=self.nino,
            ubicacion=punto,
            dentro_area_segura=False
        )
        
        alerta = Alerta.objects.create(
            nino=self.nino,
            tipo_alerta='SALIDA_AREA',
            posicion_gps=posicion,
            mensaje='Test alerta'
        )
        
        url = '/api/mis-alertas/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], alerta.id)
