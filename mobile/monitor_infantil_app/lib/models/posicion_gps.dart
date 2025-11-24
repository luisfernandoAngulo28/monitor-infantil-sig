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
    final coords = json['geometry']['coordinates'];
    final lng = coords[0] as double;
    final lat = coords[1] as double;

    return PosicionGPS(
      id: json['id'],
      ubicacion: LatLng(lat, lng),
      timestamp: DateTime.parse(json['properties']['timestamp']),
      dentroAreaSegura: json['properties']['dentro_area_segura'],
      precisionMetros: json['properties']['precision_metros']?.toDouble(),
      nivelBateria: json['properties']['nivel_bateria'],
    );
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
    return EstadoNino(
      ninoId: json['nino']['id'],
      ninoNombre: json['nino']['nombre_completo'],
      ultimaPosicion: json['ultima_posicion'] != null
          ? PosicionGPS.fromJson(json['ultima_posicion'])
          : null,
      dentroAreaSegura: json['dentro_area_segura'] ?? true,
      alertasActivas: json['alertas_activas'],
      nivelBateria: json['nivel_bateria'],
    );
  }
}
