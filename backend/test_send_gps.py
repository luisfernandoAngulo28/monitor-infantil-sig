"""
Script para enviar actualizaciones GPS de prueba al WebSocket.
Ejecutar desde el servidor con: python manage.py shell < test_send_gps.py
"""
import asyncio
import json
from channels.layers import get_channel_layer
from datetime import datetime

async def send_test_gps():
    channel_layer = get_channel_layer()
    
    # Enviar posición GPS de prueba para niño ID 1
    await channel_layer.group_send(
        'tutor_1_tracking',
        {
            'type': 'gps_update',
            'nino_id': 1,
            'lat': -17.7833,
            'lng': -63.1812,
            'dentro_area': True,
            'nivel_bateria': 85,
            'timestamp': datetime.now().isoformat()
        }
    )
    print("✅ GPS update enviado para niño 1")
    
    # Enviar otra posición para niño ID 3
    await channel_layer.group_send(
        'tutor_1_tracking',
        {
            'type': 'gps_update',
            'nino_id': 3,
            'lat': -17.7840,
            'lng': -63.1820,
            'dentro_area': False,
            'nivel_bateria': 45,
            'timestamp': datetime.now().isoformat()
        }
    )
    print("✅ GPS update enviado para niño 3 (FUERA DEL ÁREA)")

asyncio.run(send_test_gps())
