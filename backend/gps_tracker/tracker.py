#!/usr/bin/env python3
"""
GPS Tracker Worker - Chinese GPS Device Integration (xtgps.top)
================================================================

Script de producción para consultar la API del fabricante chino (xtgps.top),
extraer datos GPS mediante ingeniería inversa y enviarlos al backend Django.

IMPLEMENTACIÓN DE INGENIERÍA INVERSA:
- URL: https://www.xtgps.top/APP/AppJson.asp
- Método: POST con firma MD5
- Autenticación: APP_ID + TOKEN + Cookie de sesión
- Parseo: JSON malformado que requiere limpieza

Autor: Monitor Infantil SIG Team
Fecha: Diciembre 2024
"""

import os
import sys
import time
import json
import random
import hashlib
import requests
from datetime import datetime
from typing import Dict, Optional, Any

# ============================================================================
# CONFIGURACIÓN DE INGENIERÍA INVERSA - API CHINA (xtgps.top)
# ============================================================================

# URL de la API del fabricante chino
CHINESE_API_URL = "https://www.xtgps.top/APP/AppJson.asp"

# Credenciales de autenticación (valores que funcionan)
APP_ID = "d3d3Lnh0Z3BzLnRvcC8v"  # Base64 de 'xtgps.top'
TOKEN = "UHJvY19HZXRMYXN0UG9zaXRpb24RTic1NjIxMTQ1MjA4MycRERs0"  # GetLastPosition

# IMEI del dispositivo GPS a consultar
DEVICE_IMEI = os.getenv('DEVICE_IMEI', '56211452083')

# Cookie de sesión (DEBE SER CONFIGURADA - obtener del navegador)
# Formato esperado: "ASPSESSIONIDQCQDCDTB=XXXXXXXX; path=/"
# INSTRUCCIÓN: Copiar la cookie desde el navegador después de hacer login
# en www.xtgps.top y pegarla aquí o configurarla como variable de entorno
COOKIE_STRING = os.getenv('GPS_COOKIE', '')

# Headers HTTP requeridos para que la API acepte la conexión
HTTP_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Origin': 'https://www.xtgps.top',
    'Referer': 'https://www.xtgps.top/index.html',
    'X-Requested-With': 'XMLHttpRequest',
}

# URL del backend Django (interno en Docker: web_backend:8000)
DJANGO_API_URL = os.getenv('API_URL', 'http://web_backend:8000/api/ingesta/gps-chino/')

# Intervalo de consulta en segundos (default: 30s)
POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', '30'))

# ============================================================================
# LOGGER CON COLORES Y EMOJIS
# ============================================================================

class ColoredLogger:
    """Logger con formato visual mejorado para Docker logs"""
    
    @staticmethod
    def _timestamp():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def info(msg: str):
        print(f"ℹ️  [{ColoredLogger._timestamp()}] INFO: {msg}", flush=True)
    
    @staticmethod
    def success(msg: str):
        print(f"✅ [{ColoredLogger._timestamp()}] SUCCESS: {msg}", flush=True)
    
    @staticmethod
    def warning(msg: str):
        print(f"⚠️  [{ColoredLogger._timestamp()}] WARNING: {msg}", flush=True)
    
    @staticmethod
    def error(msg: str):
        print(f"❌ [{ColoredLogger._timestamp()}] ERROR: {msg}", flush=True)
    
    @staticmethod
    def data(msg: str):
        print(f"📊 [{ColoredLogger._timestamp()}] DATA: {msg}", flush=True)
    
    @staticmethod
    def critical(msg: str):
        print(f"🚨 [{ColoredLogger._timestamp()}] CRITICAL: {msg}", flush=True)

logger = ColoredLogger()


# ============================================================================
# FUNCIONES DE INGENIERÍA INVERSA
# ============================================================================

def generate_md5_signature(timestamp_ms: int, random_int: int, imei: str) -> str:
    """
    Genera la firma MD5 requerida por la API china
    
    Algoritmo: MD5(timestamp_ms + random_int + IMEI + APP_ID + TOKEN)
    
    Args:
        timestamp_ms: Timestamp en milisegundos
        random_int: Número aleatorio entero
        imei: IMEI del dispositivo
    
    Returns:
        Hash MD5 en hexadecimal
    """
    signature_string = f"{timestamp_ms}{random_int}{imei}{APP_ID}{TOKEN}"
    md5_hash = hashlib.md5(signature_string.encode('utf-8')).hexdigest()
    return md5_hash


def fix_malformed_json(raw_response: str) -> str:
    """
    Limpia respuestas JSON malformadas de la API china
    
    La API a veces devuelve JSONs con estructuras como: ...}{...
    Esta función intenta reparar estos casos.
    
    Args:
        raw_response: String de respuesta cruda de la API
    
    Returns:
        String JSON limpio y parseable
    """
    # Eliminar espacios en blanco al inicio y final
    cleaned = raw_response.strip()
    
    # Si hay múltiples objetos JSON separados por }{, tomar solo el primero
    if '}{' in cleaned:
        logger.warning("JSON malformado detectado (múltiples objetos). Tomando el primero.")
        cleaned = cleaned.split('}{')[0] + '}'
    
    # Eliminar caracteres no imprimibles o raros
    cleaned = ''.join(char for char in cleaned if char.isprintable() or char in '\n\r\t')
    
    return cleaned


def parse_gps_response(response_data: Any) -> Optional[Dict]:
    """
    Extrae datos GPS de la respuesta de la API china
    
    Estructura del array de respuesta (índices importantes):
    - Índice 2: Longitud (Longitude)
    - Índice 3: Latitud (Latitude)
    - Índice 7: Número de satélites
    - Índice 8: Nivel de batería (%)
    
    Args:
        response_data: Objeto JSON parseado de la API
    
    Returns:
        Dict con lat, lon, satellites, battery o None si hay error
    """
    try:
        # Verificar estructura de respuesta (según script que funciona)
        if not isinstance(response_data, dict):
            logger.error(f"Formato de respuesta inesperado: {type(response_data)}")
            return None
        
        # Verificar que la respuesta sea exitosa
        if response_data.get('m_isResultOk') != 1:
            error_msg = response_data.get('m_strContent', 'Error desconocido')
            logger.error(f"API retornó error: {error_msg}")
            return None
        
        # Obtener array de registros
        records = response_data.get('m_arrRecord')
        if not records or len(records) == 0:
            logger.warning("No hay registros GPS en la respuesta")
            return None
        
        # Extraer el primer registro (posición más reciente)
        position = records[0]
        
        # Validar que tengamos suficientes elementos
        if len(position) < 9:
            logger.error(f"Array de posición incompleto (esperado >= 9, recibido {len(position)})")
            return None
        
        # Extraer datos según índices conocidos
        longitude = float(position[2])
        latitude = float(position[3])
        satellites = int(position[7]) if position[7] is not None else 0
        battery = int(position[8]) if position[8] is not None else None
        
        # Validar coordenadas
        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            logger.error(f"Coordenadas inválidas: lat={latitude}, lon={longitude}")
            return None
        
        gps_data = {
            'lat': latitude,
            'lon': longitude,
            'satellites': satellites,
            'battery': battery
        }
        
        logger.data(f"GPS extraído: lat={latitude:.6f}, lon={longitude:.6f}, "
                   f"sats={satellites}, battery={battery}%")
        
        return gps_data
    
    except (IndexError, ValueError, TypeError) as e:
        logger.error(f"Error al parsear respuesta GPS: {e}")
        logger.error(f"Datos recibidos: {response_data}")
        return None


# ============================================================================
# CLIENTE API CHINA (xtgps.top)
# ============================================================================

class ChineseGPSClient:
    """Cliente para consultar la API del GPS chino con ingeniería inversa"""
    
    def __init__(self, imei: str, cookie: str):
        self.imei = imei
        self.cookie = cookie
        self.session = requests.Session()
        
        # Configurar headers con cookie
        self.session.headers.update(HTTP_HEADERS)
        if cookie:
            self.session.headers['Cookie'] = cookie
    
    def get_gps_data(self) -> Optional[Dict]:
        """
        Consulta la API china y extrae los datos GPS
        
        Returns:
            Dict con lat, lon, satellites, battery o None si hay error
        """
        try:
            # Generar timestamp en milisegundos
            timestamp_ms = int(time.time() * 1000)
            
            # Generar número aleatorio (14 dígitos como en la app real)
            random_int = random.randint(10000000000000, 99999999999999)
            
            # Generar firma MD5
            signature = generate_md5_signature(timestamp_ms, random_int, self.imei)
            
            # Construir payload (nombres de campos según script que funciona)
            payload = {
                'strAppID': APP_ID,
                'strUser': self.imei,
                'nTimeStamp': str(timestamp_ms),
                'strRandom': str(random_int),
                'strSign': signature,
                'strToken': TOKEN
            }
            
            logger.info(f"🌐 Consultando API china para IMEI: {self.imei}")
            logger.data(f"Payload: Time={timestamp_ms}, Random={random_int}, Sign={signature[:16]}...")
            
            # Hacer POST request
            response = self.session.post(
                CHINESE_API_URL,
                data=payload,
                timeout=15
            )
            
            # Validar respuesta HTTP
            logger.data(f"HTTP Status: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"HTTP {response.status_code}: {response.text[:200]}")
                return None
            
            logger.success(f"Respuesta recibida ({len(response.text)} bytes)")
            
            # Debug: mostrar respuesta cruda si está vacía
            if len(response.text) == 0:
                logger.warning("⚠️  Respuesta vacía. Posibles causas:")
                logger.warning("  1. Cookie expirada o inválida")
                logger.warning("  2. IMEI sin datos GPS recientes")
                logger.warning("  3. Dispositivo apagado o sin señal")
                return None
            
            # Limpiar JSON malformado
            cleaned_json = fix_malformed_json(response.text)
            
            # Parsear JSON
            try:
                json_data = json.loads(cleaned_json)
            except json.JSONDecodeError as e:
                logger.error(f"Error al parsear JSON: {e}")
                logger.error(f"JSON recibido: {cleaned_json[:500]}")
                return None
            
            # Extraer datos GPS
            gps_data = parse_gps_response(json_data)
            
            if gps_data:
                logger.success(f"✓ GPS extraído exitosamente: {gps_data['lat']:.6f}, {gps_data['lon']:.6f}")
            else:
                logger.warning("No se pudieron extraer datos GPS de la respuesta")
            
            return gps_data
        
        except requests.exceptions.Timeout:
            logger.error("⏱️  Timeout al consultar API china (15s)")
            return None
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"🔌 Error de conexión a API china: {e}")
            return None
        
        except Exception as e:
            logger.error(f"Error inesperado en cliente chino: {e}")
            return None


# ============================================================================
# CLIENTE DJANGO BACKEND
# ============================================================================

class DjangoBackendClient:
    """Cliente para enviar datos al backend Django"""
    
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def send_gps_data(self, device_id: str, gps_data: Dict) -> bool:
        """
        Envía datos GPS al backend Django
        
        Args:
            device_id: IMEI del dispositivo
            gps_data: Dict con lat, lon, satellites, battery
        
        Returns:
            True si se envió exitosamente
        """
        payload = {
            'device_id': device_id,
            'lat': gps_data['lat'],
            'lon': gps_data['lon'],
            'satellites': gps_data['satellites'],
            'battery': gps_data.get('battery')
        }
        
        try:
            logger.info(f"📤 Enviando datos a Django: {self.api_url}")
            
            response = self.session.post(
                self.api_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                precision = data.get('precision_metros', 'N/A')
                dentro_area = data.get('dentro_area_segura', 'N/A')
                
                logger.success(f"✓ Datos enviados exitosamente")
                logger.data(f"Precisión: {precision}m, Dentro área: {dentro_area}")
                
                # Si hay alerta, mostrarla
                if 'alerta' in data:
                    logger.warning(f"🚨 ALERTA: {data['alerta']}")
                
                return True
            
            elif response.status_code == 404:
                logger.error(f"❌ Dispositivo no encontrado (IMEI: {device_id})")
                logger.error("➡️  Verifica que el campo 'dispositivo_id' del Niño coincida con el IMEI")
                return False
            
            elif response.status_code == 403:
                logger.error("❌ Tracking desactivado para este niño")
                return False
            
            elif response.status_code == 400:
                error_data = response.json()
                logger.error(f"❌ Datos inválidos: {error_data}")
                return False
            
            else:
                logger.error(f"❌ HTTP {response.status_code}: {response.text[:200]}")
                return False
        
        except requests.exceptions.ConnectionError:
            logger.error("🔌 No se pudo conectar al backend Django")
            logger.warning("➡️  Verifica que el servicio web_backend esté corriendo")
            return False
        
        except requests.exceptions.Timeout:
            logger.error("⏱️  Timeout al conectar con Django backend (10s)")
            return False
        
        except Exception as e:
            logger.error(f"Error inesperado al enviar datos: {e}")
            return False


# ============================================================================
# WORKER PRINCIPAL
# ============================================================================

def main():
    """
    Worker principal que ejecuta el ciclo de polling GPS
    """
    # Banner de inicio
    print("\n" + "=" * 70)
    print("🚀 GPS TRACKER WORKER - MONITOR INFANTIL SIG")
    print("=" * 70)
    logger.info(f"Backend Django: {DJANGO_API_URL}")
    logger.info(f"Device IMEI: {DEVICE_IMEI}")
    logger.info(f"Intervalo: {POLL_INTERVAL}s")
    logger.info(f"API China: {CHINESE_API_URL}")
    print("=" * 70 + "\n")
    
    # Validar configuración
    if not COOKIE_STRING:
        logger.warning("⚠️  Cookie no configurada (GPS_COOKIE)")
        logger.warning("➡️  Obtén la cookie desde el navegador tras hacer login en www.xtgps.top")
        logger.warning("➡️  Configura la variable GPS_COOKIE en el .env o docker-compose.yml")
        logger.info("Continuando de todos modos...")
    
    # Inicializar clientes
    chinese_client = ChineseGPSClient(imei=DEVICE_IMEI, cookie=COOKIE_STRING)
    django_client = DjangoBackendClient(api_url=DJANGO_API_URL)
    
    # Contadores
    iteration = 0
    success_count = 0
    error_count = 0
    
    logger.success("✅ Worker iniciado correctamente")
    logger.info("🔄 Iniciando ciclo de polling GPS...\n")
    
    # Loop infinito
    while True:
        try:
            iteration += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print("\n" + "-" * 70)
            logger.info(f"📍 ITERACIÓN #{iteration} - {timestamp}")
            print("-" * 70)
            
            # PASO 1: Obtener datos de la API china
            gps_data = chinese_client.get_gps_data()
            
            if gps_data is None:
                logger.warning("⚠️  No se obtuvieron datos GPS. Saltando iteración.")
                error_count += 1
            else:
                # PASO 2: Enviar al backend Django
                success = django_client.send_gps_data(DEVICE_IMEI, gps_data)
                
                if success:
                    success_count += 1
                    error_count = 0  # Reset contador de errores
                else:
                    error_count += 1
            
            # Estadísticas
            logger.data(f"📊 Estadísticas: {success_count} éxitos, {error_count} errores consecutivos")
            
            # Dormir hasta próxima iteración
            logger.info(f"💤 Durmiendo {POLL_INTERVAL}s hasta próximo polling...\n")
            time.sleep(POLL_INTERVAL)
        
        except KeyboardInterrupt:
            logger.warning("\n⚠️  Interrupción de usuario (Ctrl+C)")
            logger.info("🛑 Deteniendo worker...")
            break
        
        except Exception as e:
            logger.critical(f"🚨 Error crítico en loop principal: {e}")
            error_count += 1
            
            # Si hay demasiados errores consecutivos, esperar más tiempo
            if error_count >= 5:
                logger.warning(f"⚠️  {error_count} errores consecutivos. Esperando 60s...")
                time.sleep(60)
            else:
                time.sleep(10)
    
    # Mensaje de salida
    print("\n" + "=" * 70)
    logger.info("🏁 GPS Tracker Worker finalizado")
    logger.data(f"Total de iteraciones: {iteration}")
    logger.data(f"Total de envíos exitosos: {success_count}")
    print("=" * 70 + "\n")


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(f"🚨 Error fatal: {e}")
        sys.exit(1)
