#!/usr/bin/env python3
"""
Script de test manual para verificar el request a la API china
Permite debuggear la respuesta exacta de la API
"""

import time
import random
import hashlib
import requests
import sys

# Configuración (valores reales de la aplicación)
API_URL = "https://www.xtgps.top/APP/AppJson.asp"
APP_ID = "d3d3Lnh0Z3BzLnRvcC8v"
TOKEN = "UHJvY19EZXZpY2VNb2RlbBFOJzAnEREb"
IMEI = "56211452083"

# Cookie - PEGAR AQUÍ LA COOKIE ACTUALIZADA
COOKIE = input("Pega la cookie actual (o presiona Enter para usar la del .env): ").strip()
if not COOKIE:
    import os
    COOKIE = os.getenv('GPS_COOKIE', '')
    print(f"Usando cookie del .env: {COOKIE[:50]}...")

# Generar valores
timestamp_ms = int(time.time() * 1000)
random_int = random.randint(10000000000000, 99999999999999)  # 14 dígitos como en la app

# Firma MD5
signature_string = f"{timestamp_ms}{random_int}{IMEI}{APP_ID}{TOKEN}"
signature = hashlib.md5(signature_string.encode('utf-8')).hexdigest()

# Headers
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/142.0.0.0 Mobile Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Origin': 'https://www.xtgps.top',
    'Referer': 'https://www.xtgps.top/',
    'Cookie': COOKIE
}

# Payload
payload = {
    'Time': str(timestamp_ms),
    'Random': str(random_int),
    'IMEI': IMEI,
    'AppID': APP_ID,
    'Token': TOKEN,
    'Sign': signature
}

print("\n" + "=" * 70)
print("🧪 TEST MANUAL - REQUEST A API CHINA")
print("=" * 70)
print("\n📊 CONFIGURACIÓN:")
print(f"  URL: {API_URL}")
print(f"  IMEI: {IMEI}")
print(f"  APP_ID: {APP_ID}")
print(f"  TOKEN: {TOKEN}")
print(f"  Cookie: {COOKIE[:50]}...")

print("\n🔐 PAYLOAD GENERADO:")
print(f"  Time: {timestamp_ms}")
print(f"  Random: {random_int}")
print(f"  Sign: {signature}")

print("\n🌐 ENVIANDO REQUEST...")

try:
    response = requests.post(API_URL, headers=headers, data=payload, timeout=15)
    
    print("\n✅ RESPUESTA RECIBIDA:")
    print(f"  Status Code: {response.status_code}")
    print(f"  Content-Length: {len(response.text)} bytes")
    print(f"  Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    
    print("\n📄 HEADERS DE RESPUESTA:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print("\n📝 BODY DE RESPUESTA:")
    if len(response.text) > 0:
        print(response.text)
        
        # Intentar parsear como JSON
        try:
            import json
            data = json.loads(response.text)
            print("\n✅ JSON VÁLIDO:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print("\n⚠️  No es JSON válido o está malformado")
    else:
        print("  (vacío)")
        print("\n❌ RESPUESTA VACÍA - Posibles causas:")
        print("  1. Cookie expirada - Necesitas renovarla desde el navegador")
        print("  2. IMEI sin datos GPS recientes")
        print("  3. Dispositivo apagado o sin señal")
        print("  4. Formato de request incorrecto")
    
    print("\n" + "=" * 70)
    
    if response.status_code == 200 and len(response.text) > 0:
        print("✅ TEST EXITOSO")
    else:
        print("❌ TEST FALLIDO")
        sys.exit(1)

except requests.exceptions.Timeout:
    print("\n❌ TIMEOUT - La API no respondió en 15 segundos")
    sys.exit(1)
except requests.exceptions.ConnectionError as e:
    print(f"\n❌ ERROR DE CONEXIÓN: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERROR INESPERADO: {e}")
    sys.exit(1)
