#!/usr/bin/env python
"""
Script de prueba para WebSocket GPS Tracking.

Simula un dispositivo de niño enviando actualizaciones GPS.
"""
import asyncio
import json
import websockets
import random
from datetime import datetime

# Configuración
SERVER_URL = "ws://143.198.30.170:8000/ws/tracking/tutor/1/"
NINO_ID = 1

# Coordenadas del kinder (ejemplo Santa Cruz)
KINDER_LAT = -17.7833
KINDER_LNG = -63.1812

# Radio del área (en grados, ~100 metros)
AREA_RADIUS = 0.001


async def simulate_gps_tracking():
    """Simula el tracking GPS de un niño."""
    
    print(f"🔌 Conectando a {SERVER_URL}...")
    
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            print("✅ Conectado al servidor WebSocket")
            
            # Esperar mensaje de confirmación
            response = await websocket.recv()
            print(f"📨 Servidor: {response}")
            
            # Simular movimiento del niño
            for i in range(20):
                # Generar posición aleatoria cerca del kinder
                # 50% dentro del área, 50% fuera
                if random.random() > 0.5:
                    # Dentro del área
                    lat = KINDER_LAT + random.uniform(-AREA_RADIUS/2, AREA_RADIUS/2)
                    lng = KINDER_LNG + random.uniform(-AREA_RADIUS/2, AREA_RADIUS/2)
                    dentro = True
                else:
                    # Fuera del área
                    lat = KINDER_LAT + random.uniform(-AREA_RADIUS*2, AREA_RADIUS*2)
                    lng = KINDER_LNG + random.uniform(-AREA_RADIUS*2, AREA_RADIUS*2)
                    dentro = False
                
                # Simular nivel de batería decreciente
                nivel_bateria = max(10, 100 - (i * 3))
                
                # Crear mensaje GPS
                gps_update = {
                    "type": "gps_update",
                    "nino_id": NINO_ID,
                    "lat": lat,
                    "lng": lng,
                    "nivel_bateria": nivel_bateria
                }
                
                # Enviar al servidor
                await websocket.send(json.dumps(gps_update))
                
                estado = "✅ Dentro" if dentro else "⚠️ FUERA"
                print(f"📍 [{i+1}/20] Enviado: ({lat:.6f}, {lng:.6f}) - {estado} - 🔋 {nivel_bateria}%")
                
                # Esperar respuesta (opcional)
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    response_data = json.loads(response)
                    if response_data.get('type') == 'gps_update':
                        print(f"   ← Confirmado por servidor")
                except asyncio.TimeoutError:
                    pass
                
                # Esperar antes de la siguiente actualización (simular tiempo real)
                await asyncio.sleep(5)
            
            print("\n✅ Simulación completada")
            
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ Error de WebSocket: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_ping():
    """Prueba simple de ping/pong."""
    
    print(f"🔌 Conectando a {SERVER_URL}...")
    
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            print("✅ Conectado")
            
            # Enviar ping
            await websocket.send(json.dumps({"type": "ping"}))
            print("📤 Ping enviado")
            
            # Esperar pong
            response = await websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get('type') == 'pong':
                print(f"✅ Pong recibido: {response_data.get('timestamp')}")
            else:
                print(f"📨 Respuesta: {response}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Menú principal."""
    
    print("=" * 60)
    print("🧪 Monitor Infantil - WebSocket GPS Testing")
    print("=" * 60)
    print()
    print("Opciones:")
    print("1. Simular tracking GPS (20 actualizaciones)")
    print("2. Test de ping/pong")
    print("3. Salir")
    print()
    
    choice = input("Selecciona una opción (1-3): ").strip()
    
    if choice == "1":
        print("\n🚀 Iniciando simulación de tracking GPS...\n")
        asyncio.run(simulate_gps_tracking())
    elif choice == "2":
        print("\n🏓 Probando ping/pong...\n")
        asyncio.run(test_ping())
    elif choice == "3":
        print("👋 ¡Hasta luego!")
    else:
        print("❌ Opción inválida")


if __name__ == "__main__":
    main()
