"""
Traccar GPS Integration Service

Servicio para interactuar con Traccar GPS Server API.
Permite registrar dispositivos, consultar posiciones y sincronizar datos.
"""
import requests
from typing import List, Optional, Dict, Any
from datetime import datetime
from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import logging

from .models import Nino, PosicionGPS

logger = logging.getLogger(__name__)


class TraccarAPIException(Exception):
    """Excepción personalizada para errores de Traccar API"""
    pass


class TraccarService:
    """
    Servicio para interactuar con Traccar GPS Server API.
    
    Funcionalidades:
    - Autenticación con Traccar Server
    - Registro de dispositivos
    - Consulta de posiciones GPS
    - Sincronización automática hacia Django
    """
    
    def __init__(self):
        self.base_url = settings.TRACCAR_SERVER_URL
        self.username = settings.TRACCAR_USERNAME
        self.password = settings.TRACCAR_PASSWORD
        self.session = None
        self._cookies = None
    
    def authenticate(self) -> bool:
        """
        Autenticar con Traccar server usando credenciales.
        
        Returns:
            bool: True si la autenticación fue exitosa
        
        Raises:
            TraccarAPIException: Si la autenticación falla
        """
        try:
            url = f"{self.base_url}/session"
            response = requests.post(
                url,
                data={
                    'email': self.username,
                    'password': self.password
                },
                timeout=10
            )
            
            if response.status_code == 200:
                self._cookies = response.cookies
                user_data = response.json()
                logger.info(f"✅ Autenticación exitosa con Traccar: {user_data.get('name')}")
                return True
            else:
                logger.error(f"❌ Error de autenticación: {response.status_code} - {response.text}")
                raise TraccarAPIException(f"Authentication failed: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error de conexión con Traccar: {e}")
            raise TraccarAPIException(f"Connection error: {str(e)}")
    
    def _ensure_authenticated(self):
        """Asegurar que hay una sesión autenticada válida"""
        if not self._cookies:
            self.authenticate()
    
    def get_devices(self) -> List[Dict[str, Any]]:
        """
        Obtener todos los dispositivos registrados en Traccar.
        
        Returns:
            List[Dict]: Lista de dispositivos con sus propiedades
        """
        self._ensure_authenticated()
        
        try:
            url = f"{self.base_url}/devices"
            response = requests.get(
                url,
                cookies=self._cookies,
                timeout=10
            )
            
            if response.status_code == 200:
                devices = response.json()
                logger.info(f"📱 {len(devices)} dispositivos encontrados en Traccar")
                return devices
            else:
                logger.error(f"❌ Error al obtener dispositivos: {response.status_code}")
                return []
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error al consultar dispositivos: {e}")
            return []
    
    def get_device_by_unique_id(self, unique_id: str) -> Optional[Dict[str, Any]]:
        """
        Buscar un dispositivo por su uniqueId (IMEI).
        
        Args:
            unique_id: Identificador único del dispositivo (IMEI)
        
        Returns:
            Dict con datos del dispositivo o None si no existe
        """
        devices = self.get_devices()
        
        for device in devices:
            if device.get('uniqueId') == unique_id:
                return device
        
        return None
    
    def register_device(self, device_id: str, name: str, category: str = 'person') -> Optional[int]:
        """
        Registrar un nuevo dispositivo en Traccar.
        
        Args:
            device_id: Identificador único del dispositivo (IMEI)
            name: Nombre descriptivo del dispositivo
            category: Categoría del dispositivo (person, car, etc.)
        
        Returns:
            int: ID interno de Traccar si se registró exitosamente, None en caso contrario
        """
        self._ensure_authenticated()
        
        # Verificar si ya existe
        existing = self.get_device_by_unique_id(device_id)
        if existing:
            logger.info(f"📱 Dispositivo {device_id} ya existe en Traccar (ID: {existing['id']})")
            return existing['id']
        
        try:
            url = f"{self.base_url}/devices"
            payload = {
                'name': name,
                'uniqueId': device_id,
                'category': category
            }
            
            response = requests.post(
                url,
                json=payload,
                cookies=self._cookies,
                timeout=10
            )
            
            if response.status_code == 200:
                device_data = response.json()
                logger.info(f"✅ Dispositivo registrado en Traccar: {name} (ID: {device_data['id']})")
                return device_data['id']
            else:
                logger.error(f"❌ Error al registrar dispositivo: {response.status_code} - {response.text}")
                return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error al registrar dispositivo: {e}")
            return None
    
    def get_device_positions(self, device_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtener las últimas posiciones GPS de un dispositivo específico.
        
        Args:
            device_id: Identificador único del dispositivo (IMEI)
            limit: Número máximo de posiciones a retornar
        
        Returns:
            List[Dict]: Lista de posiciones GPS
        """
        self._ensure_authenticated()
        
        # Primero obtener el ID interno de Traccar
        device = self.get_device_by_unique_id(device_id)
        if not device:
            logger.warning(f"⚠️ Dispositivo {device_id} no encontrado en Traccar")
            return []
        
        traccar_device_id = device['id']
        
        try:
            url = f"{self.base_url}/positions"
            params = {
                'deviceId': traccar_device_id
            }
            
            response = requests.get(
                url,
                params=params,
                cookies=self._cookies,
                timeout=10
            )
            
            if response.status_code == 200:
                positions = response.json()
                # Limitar resultados y ordenar por más reciente
                positions = sorted(
                    positions,
                    key=lambda p: p.get('deviceTime', ''),
                    reverse=True
                )[:limit]
                
                logger.info(f"📍 {len(positions)} posiciones obtenidas para dispositivo {device_id}")
                return positions
            else:
                logger.error(f"❌ Error al obtener posiciones: {response.status_code}")
                return []
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error al consultar posiciones: {e}")
            return []
    
    def get_latest_position(self, device_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtener la última posición GPS de un dispositivo.
        
        Args:
            device_id: Identificador único del dispositivo (IMEI)
        
        Returns:
            Dict con datos de la posición o None
        """
        positions = self.get_device_positions(device_id, limit=1)
        return positions[0] if positions else None
    
    def sync_position_to_django(
        self,
        nino: Nino,
        position_data: Dict[str, Any]
    ) -> Optional[PosicionGPS]:
        """
        Sincronizar una posición de Traccar hacia el modelo Django PosicionGPS.
        
        Args:
            nino: Instancia del modelo Nino
            position_data: Diccionario con datos de posición de Traccar
        
        Returns:
            PosicionGPS creada o None si falla
        """
        try:
            # Parsear timestamp
            device_time = position_data.get('deviceTime') or position_data.get('fixTime')
            if isinstance(device_time, str):
                timestamp = parse_datetime(device_time)
                if timestamp:
                    # Asegurar que tenga timezone
                    if timezone.is_naive(timestamp):
                        timestamp = timezone.make_aware(timestamp)
            else:
                timestamp = timezone.now()
            
            # Verificar si ya existe esta posición (evitar duplicados)
            existing = PosicionGPS.objects.filter(
                nino=nino,
                timestamp=timestamp
            ).first()
            
            if existing:
                logger.debug(f"⏭️ Posición duplicada ignorada para {nino.nombre_completo()} - {timestamp}")
                return existing
            
            # Crear punto geográfico (PostGIS usa lon, lat)
            lat = float(position_data['latitude'])
            lon = float(position_data['longitude'])
            punto_gps = Point(lon, lat, srid=4326)
            
            # Extraer metadatos adicionales
            attributes = position_data.get('attributes', {})
            battery_level = attributes.get('batteryLevel')
            if battery_level is not None:
                battery_level = int(float(battery_level))
            
            # Crear registro de posición GPS
            posicion = PosicionGPS.objects.create(
                nino=nino,
                ubicacion=punto_gps,
                precision_metros=position_data.get('accuracy'),
                altitud=position_data.get('altitude'),
                velocidad_kmh=position_data.get('speed'),
                nivel_bateria=battery_level,
                timestamp=timestamp
            )
            
            logger.info(
                f"✅ Posición sincronizada: {nino.nombre_completo()} - "
                f"({lat:.6f}, {lon:.6f}) - "
                f"{'🟢 Seguro' if posicion.dentro_area_segura else '🔴 Fuera'}"
            )
            
            return posicion
        
        except Exception as e:
            logger.error(f"❌ Error al sincronizar posición: {e}")
            return None
    
    def sync_all_positions(self) -> Dict[str, int]:
        """
        Sincronizar posiciones de todos los niños con tracking activo.
        
        Returns:
            Dict con estadísticas: {'synced': N, 'errors': M, 'skipped': K}
        """
        stats = {'synced': 0, 'errors': 0, 'skipped': 0}
        
        # Obtener niños con tracking activo y dispositivo configurado
        ninos = Nino.objects.filter(
            activo=True,
            tracking_activo=True,
            dispositivo_id__isnull=False
        ).exclude(dispositivo_id='')
        
        logger.info(f"🔄 Iniciando sincronización de {ninos.count()} niños...")
        
        for nino in ninos:
            try:
                # Obtener última posición desde Traccar
                position = self.get_latest_position(nino.dispositivo_id)
                
                if not position:
                    logger.debug(f"⏭️ No hay posiciones para {nino.nombre_completo()}")
                    stats['skipped'] += 1
                    continue
                
                # Sincronizar a Django
                result = self.sync_position_to_django(nino, position)
                
                if result:
                    stats['synced'] += 1
                else:
                    stats['errors'] += 1
            
            except Exception as e:
                logger.error(f"❌ Error al sincronizar {nino.nombre_completo()}: {e}")
                stats['errors'] += 1
        
        logger.info(
            f"✅ Sincronización completada: "
            f"{stats['synced']} nuevas, "
            f"{stats['skipped']} sin cambios, "
            f"{stats['errors']} errores"
        )
        
        return stats
    
    def delete_device(self, device_id: str) -> bool:
        """
        Eliminar un dispositivo de Traccar.
        
        Args:
            device_id: Identificador único del dispositivo (IMEI)
        
        Returns:
            bool: True si se eliminó exitosamente
        """
        self._ensure_authenticated()
        
        device = self.get_device_by_unique_id(device_id)
        if not device:
            logger.warning(f"⚠️ Dispositivo {device_id} no encontrado")
            return False
        
        try:
            url = f"{self.base_url}/devices/{device['id']}"
            response = requests.delete(
                url,
                cookies=self._cookies,
                timeout=10
            )
            
            if response.status_code == 204:
                logger.info(f"✅ Dispositivo {device_id} eliminado de Traccar")
                return True
            else:
                logger.error(f"❌ Error al eliminar dispositivo: {response.status_code}")
                return False
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error al eliminar dispositivo: {e}")
            return False
