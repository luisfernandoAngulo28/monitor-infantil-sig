#!/usr/bin/env python3
"""
Script de prueba para validar el algoritmo de firma MD5
y la estructura de la petición a la API china
"""

import time
import random
import hashlib

# Configuración (valores reales de la aplicación)
APP_ID = "d3d3Lnh0Z3BzLnRvcC8v"  # strAppID
TOKEN = "UHJvY19EZXZpY2VNb2RlbBFOJzAnEREb"  # strToken (DeviceModel)
IMEI = "56211452083"  # strUser

def generate_md5_signature(timestamp_ms: int, random_int: int, imei: str) -> str:
    """Genera la firma MD5 requerida por la API"""
    signature_string = f"{timestamp_ms}{random_int}{imei}{APP_ID}{TOKEN}"
    md5_hash = hashlib.md5(signature_string.encode('utf-8')).hexdigest()
    return md5_hash

def test_signature():
    """Prueba la generación de firma"""
    print("=" * 70)
    print("🧪 TEST - Algoritmo de Firma MD5 para API China")
    print("=" * 70)
    
    # Generar valores
    timestamp_ms = int(time.time() * 1000)
    random_int = random.randint(1000, 99999)
    
    # Generar firma
    signature = generate_md5_signature(timestamp_ms, random_int, IMEI)
    
    # Construir payload
    payload = {
        'Time': str(timestamp_ms),
        'Random': str(random_int),
        'IMEI': IMEI,
        'AppID': APP_ID,
        'Token': TOKEN,
        'Sign': signature
    }
    
    print("\n📊 VALORES GENERADOS:")
    print(f"  Timestamp (ms): {timestamp_ms}")
    print(f"  Random: {random_int}")
    print(f"  IMEI: {IMEI}")
    print(f"  APP_ID: {APP_ID}")
    print(f"  TOKEN: {TOKEN[:30]}...")
    
    print("\n🔐 FIRMA MD5:")
    print(f"  String a firmar: {timestamp_ms}{random_int}{IMEI}{APP_ID}{TOKEN}")
    print(f"  Firma MD5: {signature}")
    
    print("\n📤 PAYLOAD PARA API:")
    for key, value in payload.items():
        if key in ['AppID', 'Token', 'Sign']:
            print(f"  {key}: {value[:30]}..." if len(str(value)) > 30 else f"  {key}: {value}")
        else:
            print(f"  {key}: {value}")
    
    print("\n✅ Test completado exitosamente")
    print("=" * 70)
    
    # URL y headers
    print("\n🌐 CONFIGURACIÓN DE REQUEST:")
    print(f"  URL: https://www.xtgps.top/APP/AppJson.asp")
    print(f"  Method: POST")
    print(f"  Content-Type: application/x-www-form-urlencoded; charset=UTF-8")
    print(f"  User-Agent: Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36...")
    
    print("\n💡 NOTA: Necesitas agregar el header 'Cookie' con tu sesión activa")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    test_signature()
