#!/usr/bin/env python3
"""
Traccar GPS Poller - Polling de datos GPS desde Traccar Server
===============================================================

Script para consultar Traccar Server y enviar actualizaciones al backend Django
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
from typing import Dict, Optional

# Configuración
TRACCAR_URL = os.getenv('TRACCAR_SERVER_URL', 'http://localhost:8082/api')
TRACCAR_USER = os.getenv('TRACCAR_USERNAME', 'admin')
TRACCAR_PASS = os.getenv('TRACCAR_PASSWORD', 'admin')
DJANGO_API_URL = os.getenv('API_URL', 'http://localhost:8000/api/ingesta/gps-traccar/')
POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', '5'))  # 5 segundos

print(f"🚀 Traccar GPS Poller iniciado")
print(f"📡 Traccar Server: {TRACCAR_URL}")
print(f"🔄 Intervalo de polling: {POLL_INTERVAL}s")
print("=" * 80)

# Almacenar última posición conocida para evitar duplicados
last_positions = {}

def get_traccar_devices():
    """Obtener lista de dispositivos de Traccar"""
    try:
        response = requests.get(
            f"{TRACCAR_URL}/devices",
            auth=(TRACCAR_USER, TRACCAR_PASS),
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error obteniendo dispositivos: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return []

def get_traccar_position(device_id):
    """Obtener última posición de un dispositivo"""
    try:
        response = requests.get(
            f"{TRACCAR_URL}/positions",
            params={'deviceId': device_id},
            auth=(TRACCAR_USER, TRACCAR_PASS),
            timeout=10
        )
        if response.status_code == 200:
            positions = response.json()
            return positions[0] if positions else None
        return None
    except Exception as e:
        print(f"❌ Error obteniendo posición: {e}")
        return None

def send_to_django(device_unique_id, position_data):
    """Enviar datos al backend Django"""
    try:
        payload = {
            'imei': device_unique_id,
            'latitud': position_data['latitude'],
            'longitud': position_data['longitude'],
            'precision_metros': position_data.get('accuracy', 10.0),
            'nivel_bateria': int(position_data.get('attributes', {}).get('batteryLevel', 0)),
            'velocidad_kmh': position_data.get('speed', 0) * 1.852,  # knots to km/h
            'timestamp': position_data['fixTime']
        }
        
        response = requests.post(
            DJANGO_API_URL,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 201:
            print(f"✅ Datos enviados: {device_unique_id} -> {payload['latitud']}, {payload['longitud']}")
            return True
        else:
            print(f"❌ Error enviando datos: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error enviando a Django: {e}")
        return False

def main():
    """Loop principal"""
    iteration = 0
    
    while True:
        iteration += 1
        print(f"\n{'='*80}")
        print(f"📍 ITERACIÓN #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # Obtener dispositivos
        devices = get_traccar_devices()
        
        if not devices:
            print("⚠️  No hay dispositivos disponibles")
        else:
            print(f"📱 Dispositivos encontrados: {len(devices)}")
            
            for device in devices:
                device_id = device['id']
                device_name = device['name']
                unique_id = device['uniqueId']
                status = device['status']
                
                print(f"\n   🔍 {device_name} (ID: {unique_id}) - Status: {status}")
                
                if status == 'offline':
                    print(f"      ⏸️  Dispositivo offline, saltando...")
                    continue
                
                # Obtener última posición
                position = get_traccar_position(device_id)
                
                if not position:
                    print(f"      ⚠️  Sin datos de posición")
                    continue
                
                # Verificar si es una posición nueva
                position_id = position['id']
                last_known = last_positions.get(unique_id)
                
                if last_known == position_id:
                    print(f"      ⏭️  Sin cambios desde última consulta")
                    continue
                
                # Nueva posición detectada
                lat = position['latitude']
                lon = position['longitude']
                fix_time = position['fixTime']
                
                print(f"      📍 Nueva posición: {lat}, {lon}")
                print(f"      🕐 Timestamp: {fix_time}")
                
                # Enviar al backend
                if send_to_django(unique_id, position):
                    last_positions[unique_id] = position_id
        
        print(f"\n💤 Durmiendo {POLL_INTERVAL}s hasta próximo polling...")
        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Detenido por usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n🚨 Error crítico: {e}")
        sys.exit(1)
