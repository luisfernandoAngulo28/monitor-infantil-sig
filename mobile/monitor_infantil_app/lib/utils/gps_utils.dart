import 'dart:math';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';

/// Utilidades para manejo de GPS y cálculos geográficos.
class GpsUtils {
  /// Obtiene stream de posiciones GPS de alta precisión.
  /// 
  /// Configuración optimizada para tracking de niños:
  /// - Precisión: BEST (±1-5 metros)
  /// - Actualiza cada 5 metros de movimiento
  /// - Intervalo mínimo: 3 segundos
  static Stream<Position> getHighPrecisionStream() {
    const LocationSettings settings = LocationSettings(
      accuracy: LocationAccuracy.best, // Máxima precisión
      distanceFilter: 5, // Actualizar cada 5 metros
      timeLimit: Duration(seconds: 3), // Mínimo cada 3 segundos
    );
    
    return Geolocator.getPositionStream(locationSettings: settings);
  }

  /// Obtiene stream de posiciones GPS con precisión balanceada.
  /// 
  /// Configuración para ahorro de batería:
  /// - Precisión: HIGH (±5-15 metros)
  /// - Actualiza cada 10 metros
  /// - Intervalo mínimo: 10 segundos
  static Stream<Position> getBalancedStream() {
    const LocationSettings settings = LocationSettings(
      accuracy: LocationAccuracy.high,
      distanceFilter: 10,
      timeLimit: Duration(seconds: 10),
    );
    
    return Geolocator.getPositionStream(locationSettings: settings);
  }

  /// Calcula la rotación (ángulo) entre dos puntos GPS.
  /// 
  /// Útil para rotar marcadores en el mapa según la dirección del movimiento.
  /// 
  /// Returns: Ángulo en grados (0-360)
  /// - 0°: Norte
  /// - 90°: Este
  /// - 180°: Sur
  /// - 270°: Oeste
  static double calculateRotation(LatLng from, LatLng to) {
    double deltaLng = to.longitude - from.longitude;
    double deltaLat = to.latitude - from.latitude;

    double angle = atan2(deltaLng, deltaLat) * (180 / pi);
    return (angle + 360) % 360; // Asegurar ángulo positivo 0-360
  }

  /// Calcula distancia en metros entre dos coordenadas GPS.
  static double distanceBetween(LatLng pos1, LatLng pos2) {
    return Geolocator.distanceBetween(
      pos1.latitude,
      pos1.longitude,
      pos2.latitude,
      pos2.longitude,
    );
  }

  /// Verifica si los servicios de ubicación están habilitados.
  static Future<bool> isLocationServiceEnabled() async {
    return await Geolocator.isLocationServiceEnabled();
  }

  /// Solicita permisos de ubicación al usuario.
  static Future<LocationPermission> requestPermission() async {
    return await Geolocator.requestPermission();
  }

  /// Verifica el estado actual de permisos de ubicación.
  static Future<LocationPermission> checkPermission() async {
    return await Geolocator.checkPermission();
  }

  /// Abre configuración de ubicación del dispositivo.
  static Future<bool> openLocationSettings() async {
    return await Geolocator.openLocationSettings();
  }

  /// Convierte Position a LatLng (para Google Maps).
  static LatLng positionToLatLng(Position position) {
    return LatLng(position.latitude, position.longitude);
  }

  /// Formatea coordenadas para mostrar al usuario.
  /// Ejemplo: "-17.7833, -63.1812"
  static String formatCoordinates(LatLng position, {int decimals = 4}) {
    return '${position.latitude.toStringAsFixed(decimals)}, '
           '${position.longitude.toStringAsFixed(decimals)}';
  }

  /// Calcula velocidad en km/h desde dos posiciones GPS.
  static double calculateSpeed(
    Position from,
    Position to,
    Duration timeDiff,
  ) {
    double distanceMeters = Geolocator.distanceBetween(
      from.latitude,
      from.longitude,
      to.latitude,
      to.longitude,
    );

    double timeHours = timeDiff.inSeconds / 3600;
    return (distanceMeters / 1000) / timeHours; // km/h
  }

  /// Verifica si una posición GPS es válida.
  static bool isValidPosition(Position? position) {
    if (position == null) return false;
    
    // Verificar que las coordenadas estén en rangos válidos
    if (position.latitude < -90 || position.latitude > 90) return false;
    if (position.longitude < -180 || position.longitude > 180) return false;
    
    // Verificar precisión razonable (menos de 50 metros)
    if (position.accuracy > 50) return false;
    
    return true;
  }
}
