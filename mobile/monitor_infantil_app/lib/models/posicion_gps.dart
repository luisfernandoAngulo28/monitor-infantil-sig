import 'package:latlong2/latlong.dart';

class PosicionGPS {
  final int id;
  final LatLng ubicacion;
  final DateTime timestamp;
  final bool dentroAreaSegura;
  final double? precisionMetros;
  final int? nivelBateria;

  PosicionGPS({
    required this.id,
    required this.ubicacion,
    required this.timestamp,
    required this.dentroAreaSegura,
    this.precisionMetros,
    this.nivelBateria,
  });

  factory PosicionGPS.fromJson(Map<String, dynamic> json) {
    // Detectar formato GeoJSON (PosicionGPSSerializer) vs formato simple (PosicionGPSSimpleSerializer)
    if (json.containsKey('geometry')) {
      // Formato GeoJSON
      final coords = json['geometry']['coordinates'];
      final lng = coords[0] as double;
      final lat = coords[1] as double;

      return PosicionGPS(
        id: json['id'],
        ubicacion: LatLng(lat, lng),
        timestamp: DateTime.parse(json['properties']['timestamp']),
        dentroAreaSegura: json['properties']['dentro_area_segura'] ?? false,
        precisionMetros: json['properties']['precision_metros']?.toDouble(),
        nivelBateria: json['properties']['nivel_bateria'],
      );
    } else {
      // Formato simple
      final lat = json['latitud'] as double?;
      final lng = json['longitud'] as double?;

      return PosicionGPS(
        id: json['id'],
        ubicacion: LatLng(lat ?? 0.0, lng ?? 0.0),
        timestamp: DateTime.parse(json['timestamp']),
        dentroAreaSegura: json['dentro_area_segura'] ?? false,
        precisionMetros: json['precision_metros']?.toDouble(),
        nivelBateria: json['nivel_bateria'],
      );
    }
  }
}

class EstadoNino {
  final int ninoId;
  final String ninoNombre;
  final PosicionGPS? ultimaPosicion;
  final bool dentroAreaSegura;
  final int alertasActivas;
  final int? nivelBateria;

  EstadoNino({
    required this.ninoId,
    required this.ninoNombre,
    this.ultimaPosicion,
    required this.dentroAreaSegura,
    required this.alertasActivas,
    this.nivelBateria,
  });

  factory EstadoNino.fromJson(Map<String, dynamic> json) {
    final nino = json['nino'];
    final nombreCompleto = nino['nombre_completo'] ?? 
                           '${nino['nombre'] ?? ''} ${nino['apellido_paterno'] ?? ''}'.trim();
    
    return EstadoNino(
      ninoId: nino['id'],
      ninoNombre: nombreCompleto.isEmpty ? 'Niño sin nombre' : nombreCompleto,
      ultimaPosicion: json['ultima_posicion'] != null
          ? PosicionGPS.fromJson(json['ultima_posicion'])
          : null,
      dentroAreaSegura: json['dentro_area_segura'] ?? true,
      alertasActivas: json['alertas_activas'] ?? 0,
      nivelBateria: json['nivel_bateria'],
    );
  }
}
