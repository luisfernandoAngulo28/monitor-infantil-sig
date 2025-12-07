import 'package:flutter/foundation.dart';
import 'dart:async';
import 'package:geolocator/geolocator.dart';
import '../services/websocket_service.dart';
import '../models/posicion_gps.dart';
import '../utils/gps_utils.dart';

/// Provider para manejar el estado de GPS tracking en tiempo real.
/// 
/// Integra el WebSocketService con el estado de la aplicación,
/// permitiendo actualizar el mapa automáticamente cuando llegan
/// nuevas posiciones GPS.
class GPSTrackingProvider with ChangeNotifier {
  final WebSocketService _wsService = WebSocketService();
  StreamSubscription<Map<String, dynamic>>? _messageSubscription;
  StreamSubscription<Position>? _gpsStreamSubscription;

  // Estado
  bool _isConnected = false;
  Map<int, PosicionGPS> _latestPositions = {};
  List<String> _recentAlerts = [];
  Position? _currentPosition;
  bool _isTrackingEnabled = false;

  // Getters
  bool get isConnected => _isConnected;
  Map<int, PosicionGPS> get latestPositions => _latestPositions;
  List<String> get recentAlerts => _recentAlerts;
  Position? get currentPosition => _currentPosition;
  bool get isTrackingEnabled => _isTrackingEnabled;

  /// Inicia tracking GPS de alta precisión.
  /// 
  /// Envía automáticamente posiciones al servidor vía WebSocket.
  Future<void> startHighPrecisionTracking(int ninoId) async {
    // Verificar permisos
    final permission = await GpsUtils.checkPermission();
    if (permission == LocationPermission.denied) {
      await GpsUtils.requestPermission();
    }

    // Verificar servicio habilitado
    final enabled = await GpsUtils.isLocationServiceEnabled();
    if (!enabled) {
      debugPrint('⚠️ Servicio de ubicación desactivado');
      return;
    }

    // Cancelar stream anterior si existe
    await _gpsStreamSubscription?.cancel();

    // Iniciar stream de alta precisión
    _gpsStreamSubscription = GpsUtils.getHighPrecisionStream().listen(
      (Position position) {
        if (!GpsUtils.isValidPosition(position)) {
          debugPrint('⚠️ Posición GPS inválida, ignorando');
          return;
        }

        _currentPosition = position;
        debugPrint('📍 GPS actualizado: ${GpsUtils.formatCoordinates(
          GpsUtils.positionToLatLng(position),
        )} - Precisión: ${position.accuracy.toStringAsFixed(1)}m');

        // Enviar al servidor vía WebSocket
        if (_isConnected) {
          sendGPSUpdate(
            ninoId: ninoId,
            lat: position.latitude,
            lng: position.longitude,
            nivelBateria: 100, // TODO: Obtener nivel real de batería
          );
        }

        notifyListeners();
      },
      onError: (error) {
        debugPrint('❌ Error en stream GPS: $error');
      },
    );

    _isTrackingEnabled = true;
    notifyListeners();
    debugPrint('✅ Tracking GPS de alta precisión iniciado para niño $ninoId');
  }

  /// Detiene el tracking GPS.
  Future<void> stopTracking() async {
    await _gpsStreamSubscription?.cancel();
    _gpsStreamSubscription = null;
    _isTrackingEnabled = false;
    _currentPosition = null;
    notifyListeners();
    debugPrint('🛑 Tracking GPS detenido');
  }
  PosicionGPS? getPositionForNino(int ninoId) {
    return _latestPositions[ninoId];
  }

  /// Conectar al servidor WebSocket
  void connect({
    required String serverUrl,
    required int tutorId,
    String? authToken,
  }) {
    debugPrint('🔌 Iniciando conexión WebSocket...');

    // Conectar al servicio
    _wsService.connect(
      serverUrl: serverUrl,
      tutorId: tutorId,
      authToken: authToken,
    );

    // Escuchar mensajes
    _messageSubscription?.cancel();
    _messageSubscription = _wsService.messages.listen(_handleMessage);

    _isConnected = true;
    notifyListeners();
  }

  /// Manejar mensajes del WebSocket
  void _handleMessage(Map<String, dynamic> data) {
    final type = data['type'];

    switch (type) {
      case 'connection_established':
        _handleConnectionEstablished(data);
        break;

      case 'gps_update':
        _handleGPSUpdate(data);
        break;

      case 'alert':
        _handleAlert(data);
        break;

      case 'error':
        _handleError(data);
        break;
    }
  }

  void _handleConnectionEstablished(Map<String, dynamic> data) {
    debugPrint('✅ Conexión establecida: ${data['message']}');
    _isConnected = true;
    notifyListeners();
  }

  void _handleGPSUpdate(Map<String, dynamic> data) {
    try {
      final ninoId = data['nino_id'] as int;
      final lat = (data['lat'] as num).toDouble();
      final lng = (data['lng'] as num).toDouble();
      final dentroArea = data['dentro_area'] as bool? ?? true;
      final nivelBateria = data['nivel_bateria'] as int? ?? 100;
      final timestamp = data['timestamp'] as String?;

      // Crear objeto PosicionGPS
      final posicion = PosicionGPS(
        id: 0, // No necesario para updates en tiempo real
        ubicacion: LatLng(lat, lng),
        timestamp: timestamp != null 
            ? DateTime.parse(timestamp) 
            : DateTime.now(),
        dentroAreaSegura: dentroArea,
        nivelBateria: nivelBateria,
      );

      // Actualizar posición en el mapa
      _latestPositions[ninoId] = posicion;

      debugPrint('📍 Posición actualizada - Niño $ninoId: ($lat, $lng) - Dentro: $dentroArea');

      // Notificar cambios a los widgets
      notifyListeners();

    } catch (e) {
      debugPrint('❌ Error al procesar GPS update: $e');
    }
  }

  void _handleAlert(Map<String, dynamic> data) {
    try {
      final mensaje = data['mensaje'] as String;
      final ninoNombre = data['nino_nombre'] as String?;

      final alertText = ninoNombre != null 
          ? '🚨 $ninoNombre: $mensaje'
          : '🚨 $mensaje';

      // Agregar a alertas recientes
      _recentAlerts.insert(0, alertText);

      // Mantener solo las últimas 10 alertas
      if (_recentAlerts.length > 10) {
        _recentAlerts.removeLast();
      }

      debugPrint('🚨 ALERTA: $alertText');

      // Notificar cambios
      notifyListeners();

    } catch (e) {
      debugPrint('❌ Error al procesar alerta: $e');
    }
  }

  void _handleError(Map<String, dynamic> data) {
    final errorMessage = data['message'] as String?;
    debugPrint('⚠️ Error del servidor: $errorMessage');
  }

  /// Enviar actualización GPS al servidor
  void sendGPSUpdate({
    required int ninoId,
    required double lat,
    required double lng,
    int nivelBateria = 100,
  }) {
    _wsService.sendGPSUpdate(
      ninoId: ninoId,
      lat: lat,
      lng: lng,
      nivelBateria: nivelBateria,
    );
  }

  /// Solicitar marcadores de prueba
  void requestTestMarkers() {
    _wsService.requestTestMarkers();
  }

  /// Limpiar alertas recientes
  void clearAlerts() {
    _recentAlerts.clear();
    notifyListeners();
  }

  /// Desconectar del WebSocket
  void disconnect() {
    debugPrint('🔌 Desconectando GPS Tracking...');
    
    _messageSubscription?.cancel();
    _messageSubscription = null;
    
    _wsService.disconnect();
    
    _isConnected = false;
    _latestPositions.clear();
    
    notifyListeners();
  }

  @override
  void dispose() {
    disconnect();
    _wsService.dispose();
    super.dispose();
  }
}
