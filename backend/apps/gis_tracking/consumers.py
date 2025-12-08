"""
WebSocket Consumers para tracking GPS en tiempo real.

Maneja las conexiones WebSocket entre el backend y las apps móviles/web
para actualizaciones GPS en tiempo real.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils import timezone
from apps.gis_tracking.models import Nino, Tutor, PosicionGPS
from django.contrib.gis.geos import Point


class GPSTrackingConsumer(AsyncWebsocketConsumer):
    """
    Consumer para manejar actualizaciones GPS en tiempo real.
    
    Cada tutor se conecta a un canal de tracking donde recibe
    actualizaciones en tiempo real de las posiciones de sus niños.
    """
    
    async def connect(self):
        """Acepta la conexión WebSocket y une al tutor a su grupo."""
        self.user = self.scope.get('user')
        
        # Obtener el tutor_id de la URL
        self.tutor_id = self.scope['url_route']['kwargs'].get('tutor_id')
        
        if not self.tutor_id:
            await self.close()
            return
        
        # En desarrollo, permitir conexiones sin autenticación
        # TODO: Agregar autenticación JWT via query params en producción
        # if self.user and self.user.is_authenticated:
        #     has_access = await self.verify_tutor_access()
        #     if not has_access:
        #         await self.close()
        #         return
        
        # Nombre del grupo de tracking para este tutor
        self.room_group_name = f'tracking_tutor_{self.tutor_id}'
        
        # Unirse al grupo de Channels
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Aceptar la conexión
        await self.accept()
        
        print(f'✅ Tutor {self.tutor_id} conectado al tracking en tiempo real')
        
        # Enviar mensaje de confirmación
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Conectado al tracking del tutor {self.tutor_id}',
            'timestamp': timezone.now().isoformat()
        }))
    
    async def disconnect(self, close_code):
        """Desconecta del grupo cuando se cierra el WebSocket."""
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            print(f'❌ Tutor {self.tutor_id} desconectado del tracking')
    
    async def receive(self, text_data):
        """
        Recibe mensajes del cliente WebSocket.
        
        Tipos de mensajes soportados:
        - gps_update: Actualización de posición GPS desde dispositivo del niño
        - ping: Mantener conexión viva
        - test_markers: Enviar marcadores de prueba
        """
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'gps_update':
                await self.handle_gps_update(data)
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': timezone.now().isoformat()
                }))
            elif message_type == 'test_markers':
                # Enviar marcadores de prueba directamente
                await self.send(text_data=json.dumps({
                    'type': 'gps_update',
                    'nino_id': 1,
                    'lat': -17.7833,
                    'lng': -63.1812,
                    'dentro_area': True,
                    'nivel_bateria': 85,
                    'timestamp': timezone.now().isoformat()
                }))
                await self.send(text_data=json.dumps({
                    'type': 'gps_update',
                    'nino_id': 3,
                    'lat': -17.7840,
                    'lng': -63.1820,
                    'dentro_area': False,
                    'nivel_bateria': 45,
                    'timestamp': timezone.now().isoformat()
                }))
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Tipo de mensaje desconocido: {message_type}'
                }))
        
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'JSON inválido'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Error al procesar mensaje: {str(e)}'
            }))
    
    async def handle_gps_update(self, data):
        """
        Procesa una actualización GPS del dispositivo del niño.
        
        Guarda la posición en la BD y la transmite a todos los tutores conectados.
        """
        try:
            nino_id = data.get('nino_id')
            lat = data.get('lat')
            lng = data.get('lng')
            nivel_bateria = data.get('nivel_bateria', 100)
            
            if not all([nino_id, lat is not None, lng is not None]):
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Faltan datos requeridos (nino_id, lat, lng)'
                }))
                return
            
            # Guardar posición en la base de datos
            posicion = await self.save_gps_position(
                nino_id, lat, lng, nivel_bateria
            )
            
            if posicion:
                # Emitir actualización a todos los tutores conectados a este niño
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'gps_position_update',
                        'nino_id': nino_id,
                        'lat': lat,
                        'lng': lng,
                        'nivel_bateria': nivel_bateria,
                        'dentro_area': posicion['dentro_area'],
                        'timestamp': posicion['timestamp']
                    }
                )
        
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Error al procesar GPS: {str(e)}'
            }))
    
    async def gps_update(self, event):
        """
        Handler para mensajes gps_update desde el channel layer.
        Enviado automáticamente cuando se guarda una PosicionGPS.
        """
        await self.send(text_data=json.dumps({
            'type': 'gps_update',
            'nino_id': event['nino_id'],
            'nino_nombre': event.get('nino_nombre'),
            'timestamp': event.get('timestamp'),
            'lat': event['lat'],
            'lng': event['lon'],  # Renombrar lon a lng para consistencia con Flutter
            'precision_metros': event.get('precision_metros'),
            'dentro_area_segura': event.get('dentro_area_segura'),
            'nivel_bateria': event.get('nivel_bateria'),
        }))
        print(f'📤 GPS update enviado al cliente: {event.get("nino_nombre")}')
    
    async def gps_position_update(self, event):
        """
        Envía actualización GPS al cliente WebSocket.
        
        Este método es llamado cuando se envía un mensaje al grupo.
        """
        await self.send(text_data=json.dumps({
            'type': 'gps_update',
            'nino_id': event['nino_id'],
            'lat': event['lat'],
            'lng': event['lng'],
            'nivel_bateria': event['nivel_bateria'],
            'dentro_area': event['dentro_area'],
            'timestamp': event['timestamp']
        }))
    
    async def alert_created(self, event):
        """
        Envía alerta en tiempo real cuando un niño sale del área.
        """
        await self.send(text_data=json.dumps({
            'type': 'alert',
            'nino_id': event['nino_id'],
            'nino_nombre': event['nino_nombre'],
            'mensaje': event['mensaje'],
            'timestamp': event['timestamp']
        }))
    
    @database_sync_to_async
    def verify_tutor_access(self):
        """Verifica que el usuario tenga acceso a este tutor."""
        try:
            tutor = Tutor.objects.get(id=self.tutor_id, usuario=self.user)
            return True
        except Tutor.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_gps_position(self, nino_id, lat, lng, nivel_bateria):
        """
        Guarda la posición GPS en la base de datos.
        
        Returns:
            dict: Información de la posición guardada, o None si hay error
        """
        try:
            nino = Nino.objects.get(id=nino_id)
            
            # Crear punto geográfico
            ubicacion = Point(lng, lat, srid=4326)
            
            # Verificar si está dentro del área del centro educativo
            dentro_area = False
            if nino.centro_educativo and nino.centro_educativo.area_permitida:
                dentro_area = nino.centro_educativo.area_permitida.contains(ubicacion)
            
            # Guardar posición
            posicion = PosicionGPS.objects.create(
                nino=nino,
                ubicacion=ubicacion,
                nivel_bateria=nivel_bateria,
                dentro_area_segura=dentro_area
            )
            
            return {
                'dentro_area': dentro_area,
                'timestamp': posicion.timestamp.isoformat()
            }
        
        except Nino.DoesNotExist:
            print(f'❌ Niño {nino_id} no encontrado')
            return None
        except Exception as e:
            print(f'❌ Error al guardar posición GPS: {str(e)}')
            return None
