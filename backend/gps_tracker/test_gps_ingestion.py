#!/usr/bin/env python3
"""
Script de Prueba para Endpoint de Ingesta GPS
==============================================

Este script prueba el endpoint /api/ingesta/gps-chino/ con diferentes escenarios.

Uso:
    python test_gps_ingestion.py
"""

import requests
import json
from datetime import datetime

# Configuración
API_URL = "http://localhost:8000/api/ingesta/gps-chino/"
DEVICE_IMEI = "862104056214397"  # Cambiar por tu IMEI real

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    """Imprime un encabezado formateado"""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")


def print_success(text):
    """Imprime mensaje de éxito"""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text):
    """Imprime mensaje de error"""
    print(f"{RED}✗ {text}{RESET}")


def print_warning(text):
    """Imprime mensaje de advertencia"""
    print(f"{YELLOW}⚠ {text}{RESET}")


def test_valid_gps_strong_signal():
    """Test 1: GPS con señal fuerte (satellites >= 3)"""
    print_header("TEST 1: GPS con señal fuerte (5 satélites)")
    
    payload = {
        "device_id": DEVICE_IMEI,
        "lat": -17.7833,
        "lon": -63.1812,
        "satellites": 5,
        "battery": 85,
        "altitude": 420.5,
        "speed": 2.5
    }
    
    print(f"📡 Enviando: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        
        print(f"\n📥 Status Code: {response.status_code}")
        print(f"📄 Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201:
            data = response.json()
            precision = data['posicion']['precision_metros']
            
            if precision == 10.0:
                print_success(f"Precisión correcta: {precision}m (señal fuerte esperada)")
            else:
                print_error(f"Precisión incorrecta: {precision}m (esperado: 10.0m)")
        else:
            print_error(f"Request falló: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {e}")


def test_valid_gps_weak_signal():
    """Test 2: GPS con señal débil (satellites < 3)"""
    print_header("TEST 2: GPS con señal débil (1 satélite)")
    
    payload = {
        "device_id": DEVICE_IMEI,
        "lat": -17.7840,
        "lon": -63.1820,
        "satellites": 1,
        "battery": 70
    }
    
    print(f"📡 Enviando: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        
        print(f"\n📥 Status Code: {response.status_code}")
        print(f"📄 Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201:
            data = response.json()
            precision = data['posicion']['precision_metros']
            
            if precision == 200.0:
                print_success(f"Precisión correcta: {precision}m (señal débil esperada)")
            else:
                print_error(f"Precisión incorrecta: {precision}m (esperado: 200.0m)")
        else:
            print_error(f"Request falló: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {e}")


def test_invalid_coordinates():
    """Test 3: Coordenadas inválidas"""
    print_header("TEST 3: Coordenadas inválidas (fuera de rango)")
    
    payload = {
        "device_id": DEVICE_IMEI,
        "lat": 95.0,  # Inválido (> 90)
        "lon": 200.0,  # Inválido (> 180)
        "satellites": 5,
        "battery": 85
    }
    
    print(f"📡 Enviando: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        
        print(f"\n📥 Status Code: {response.status_code}")
        print(f"📄 Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 400:
            print_success("Validación funcionó correctamente (400 Bad Request esperado)")
        else:
            print_warning(f"Status code inesperado: {response.status_code} (esperado: 400)")
            
    except Exception as e:
        print_error(f"Error: {e}")


def test_device_not_found():
    """Test 4: Dispositivo no encontrado"""
    print_header("TEST 4: Dispositivo no registrado (IMEI inexistente)")
    
    payload = {
        "device_id": "999999999999999",  # IMEI que no existe en BD
        "lat": -17.7833,
        "lon": -63.1812,
        "satellites": 5,
        "battery": 85
    }
    
    print(f"📡 Enviando: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        
        print(f"\n📥 Status Code: {response.status_code}")
        print(f"📄 Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 404:
            print_success("Manejo de error correcto (404 Not Found esperado)")
        else:
            print_warning(f"Status code inesperado: {response.status_code} (esperado: 404)")
            
    except Exception as e:
        print_error(f"Error: {e}")


def test_missing_fields():
    """Test 5: Campos requeridos faltantes"""
    print_header("TEST 5: Payload incompleto (sin coordenadas)")
    
    payload = {
        "device_id": DEVICE_IMEI,
        "satellites": 5,
        "battery": 85
        # Faltan lat y lon
    }
    
    print(f"📡 Enviando: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        
        print(f"\n📥 Status Code: {response.status_code}")
        print(f"📄 Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 400:
            print_success("Validación de campos requeridos funcionó (400 esperado)")
        else:
            print_warning(f"Status code inesperado: {response.status_code} (esperado: 400)")
            
    except Exception as e:
        print_error(f"Error: {e}")


def test_connection():
    """Test preliminar: Verificar conectividad con el servidor"""
    print_header("TEST PRELIMINAR: Verificar conectividad")
    
    try:
        response = requests.get(API_URL.replace('/ingesta/gps-chino/', ''), timeout=5)
        print_success(f"Servidor Django accesible (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar al servidor Django")
        print_warning(f"Verifica que Django esté corriendo en: {API_URL}")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def main():
    """Ejecuta todos los tests"""
    print(f"\n{BLUE}{'#' * 70}{RESET}")
    print(f"{BLUE}# TEST SUITE: GPS Ingestion Endpoint{RESET}")
    print(f"{BLUE}# Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{BLUE}# API URL: {API_URL}{RESET}")
    print(f"{BLUE}# Device IMEI: {DEVICE_IMEI}{RESET}")
    print(f"{BLUE}{'#' * 70}{RESET}")
    
    # Test de conectividad primero
    if not test_connection():
        print_error("\n❌ Tests abortados: No se pudo conectar al servidor")
        return
    
    # Ejecutar todos los tests
    test_valid_gps_strong_signal()
    test_valid_gps_weak_signal()
    test_invalid_coordinates()
    test_device_not_found()
    test_missing_fields()
    
    # Resumen final
    print_header("🎯 TESTS COMPLETADOS")
    print("\n📝 NOTAS IMPORTANTES:")
    print("   1. Test 1 y 2 fallarán con 404 si el IMEI no está registrado en BD")
    print("   2. Para que los tests pasen, ejecuta en Django shell:")
    print(f"\n      nino = Nino.objects.get(id=TU_ID)")
    print(f"      nino.dispositivo_id = '{DEVICE_IMEI}'")
    print("      nino.tracking_activo = True")
    print("      nino.save()")
    print(f"\n{BLUE}{'=' * 70}{RESET}\n")


if __name__ == '__main__':
    main()
