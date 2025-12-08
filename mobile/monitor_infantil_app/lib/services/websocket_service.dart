import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:flutter/foundation.dart';

/// Servicio para manejar conexiones WebSocket en tiempo real.
/// 
/// Permite recibir actualizaciones GPS instantáneas del servidor
/// sin necesidad de hacer polling HTTP.
class WebSocketService {
  static final WebSocketService _instance = WebSocketService._internal();
  factory WebSocketService() => _instance;
  WebSocketService._internal();

  WebSocketChannel? _channel;
  StreamController<Map<String, dynamic>>? _messageController;
  Timer? _reconnectTimer;
  Timer? _pingTimer;
  
  bool _isConnected = false;
  int _reconnectAttempts = 0;
  static const int _maxReconnectAttempts = 5;
  static const Duration _reconnectDelay = Duration(seconds: 3);
  static const Duration _pingInterval = Duration(seconds: 30);

  String? _serverUrl;
  int? _tutorId;
  String? _authToken;

  /// Stream de mensajes recibidos del servidor
  Stream<Map<String, dynamic>> get messages => 
      _messageController?.stream ?? const Stream.empty();

  /// Estado de conexión
  bool get isConnected => _isConnected;

  /// Conectar al servidor WebSocket
  /// 
  /// [serverUrl]: URL del servidor (ej: 'ws://143.198.30.170:8000')
  /// [tutorId]: ID del tutor para el canal de tracking
  /// [authToken]: Token JWT para autenticación
  void connect({
    required String serverUrl,
    required int tutorId,
    String? authToken,
  }) {
    _serverUrl = serverUrl;
    _tutorId = tutorId;
    _authToken = authToken;

    _initializeConnection();
  }

  void _initializeConnection() {
    if (_isConnected) {
      debugPrint('⚠️ Ya existe una conexión WebSocket activa');
      return;
    }

    try {
      // Construir URL del WebSocket
      final wsUrl = _buildWebSocketUrl();
      debugPrint('🔌 Conectando a WebSocket: $wsUrl');

      // Crear canal WebSocket
      _channel = WebSocketChannel.connect(Uri.parse(wsUrl));
      
      // Crear stream controller si no existe
      _messageController ??= StreamController<Map<String, dynamic>>.broadcast();

      // Escuchar mensajes
      _channel!.stream.listen(
        _onMessage,
        onError: _onError,
        onDone: _onDone,
        cancelOnError: false,
      );

      _isConnected = true;
      _reconnectAttempts = 0;
      
      debugPrint('✅ WebSocket conectado exitosamente');

      // Iniciar ping automático para mantener conexión viva
      _startPing();

    } catch (e) {
      debugPrint('❌ Error al conectar WebSocket: $e');
      _scheduleReconnect();
    }
  }

  String _buildWebSocketUrl() {
    // Convertir http:// a ws://
    String wsUrl = _serverUrl!.replaceFirst('http://', 'ws://');
    wsUrl = wsUrl.replaceFirst('https://', 'wss://');
    
    // Eliminar cualquier puerto :0 incorrecto
    wsUrl = wsUrl.replaceAll(':0', '');
    
    // Agregar ruta del WebSocket
    return '$wsUrl/ws/tracking/tutor/$_tutorId/';
  }

  void _onMessage(dynamic message) {
    try {
      final data = jsonDecode(message as String) as Map<String, dynamic>;
      debugPrint('📨 Mensaje WebSocket recibido: ${data['type']}');

      // Agregar al stream
      _messageController?.add(data);

      // Manejar diferentes tipos de mensajes
      switch (data['type']) {
        case 'connection_established':
          debugPrint('✅ ${data['message']}');
          break;
        
        case 'gps_update':
          debugPrint('📍 GPS Update - Niño ${data['nino_id']}: (${data['lat']}, ${data['lng']})');
          break;
        
        case 'alert':
          debugPrint('🚨 ALERTA: ${data['mensaje']}');
          break;
        
        case 'pong':
          // Respuesta a ping - conexión viva
          break;
        
        case 'error':
          debugPrint('⚠️ Error del servidor: ${data['message']}');
          break;
      }

    } catch (e) {
      debugPrint('❌ Error al procesar mensaje: $e');
    }
  }

  void _onError(error) {
    debugPrint('❌ Error en WebSocket: $error');
    _isConnected = false;
    _scheduleReconnect();
  }

  void _onDone() {
    debugPrint('🔌 Conexión WebSocket cerrada');
    _isConnected = false;
    _stopPing();
    _scheduleReconnect();
  }

  void _scheduleReconnect() {
    if (_reconnectAttempts >= _maxReconnectAttempts) {
      debugPrint('❌ Máximo de intentos de reconexión alcanzado');
      return;
    }

    _reconnectTimer?.cancel();
    _reconnectAttempts++;

    debugPrint('🔄 Reintentando conexión en ${_reconnectDelay.inSeconds}s (intento $_reconnectAttempts/$_maxReconnectAttempts)');

    _reconnectTimer = Timer(_reconnectDelay, () {
      _initializeConnection();
    });
  }

  void _startPing() {
    _stopPing();
    _pingTimer = Timer.periodic(_pingInterval, (timer) {
      if (_isConnected) {
        sendMessage({'type': 'ping'});
      }
    });
  }

  void _stopPing() {
    _pingTimer?.cancel();
    _pingTimer = null;
  }

  /// Enviar mensaje al servidor
  void sendMessage(Map<String, dynamic> message) {
    if (!_isConnected) {
      debugPrint('⚠️ No se puede enviar mensaje: WebSocket no conectado');
      return;
    }

    try {
      final jsonMessage = jsonEncode(message);
      _channel?.sink.add(jsonMessage);
      debugPrint('📤 Mensaje enviado: ${message['type']}');
    } catch (e) {
      debugPrint('❌ Error al enviar mensaje: $e');
    }
  }

  /// Enviar actualización GPS al servidor
  void sendGPSUpdate({
    required int ninoId,
    required double lat,
    required double lng,
    int nivelBateria = 100,
  }) {
    sendMessage({
      'type': 'gps_update',
      'nino_id': ninoId,
      'lat': lat,
      'lng': lng,
      'nivel_bateria': nivelBateria,
    });
  }

  /// Solicitar marcadores de prueba al servidor
  void requestTestMarkers() {
    sendMessage({'type': 'test_markers'});
    debugPrint('📍 Solicitando marcadores de prueba...');
  }

  /// Desconectar del servidor
  void disconnect() {
    debugPrint('🔌 Desconectando WebSocket...');
    
    _reconnectTimer?.cancel();
    _stopPing();
    
    _channel?.sink.close();
    _channel = null;
    
    _isConnected = false;
    _reconnectAttempts = 0;
    
    debugPrint('✅ WebSocket desconectado');
  }

  /// Limpiar recursos
  void dispose() {
    disconnect();
    _messageController?.close();
    _messageController = null;
  }
}
