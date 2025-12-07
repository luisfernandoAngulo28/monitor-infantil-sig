/// Modelo para niños cercanos obtenidos de la búsqueda espacial
class NinoCercano {
  final int id;
  final String nombre;
  final String apellidoPaterno;
  final String apellidoMaterno;
  final String nombreCompleto;
  final PosicionCercana posicion;
  final double distanciaMetros;
  final double distanciaKm;
  final String? ultimaActualizacion;
  final bool dentroAreaSegura;
  final double? velocidadKmh;
  final double? precisionMetros;
  final KinderInfo kinder;
  final String estado;
  final String estadoColor;

  NinoCercano({
    required this.id,
    required this.nombre,
    required this.apellidoPaterno,
    required this.apellidoMaterno,
    required this.nombreCompleto,
    required this.posicion,
    required this.distanciaMetros,
    required this.distanciaKm,
    this.ultimaActualizacion,
    required this.dentroAreaSegura,
    this.velocidadKmh,
    this.precisionMetros,
    required this.kinder,
    required this.estado,
    required this.estadoColor,
  });

  factory NinoCercano.fromJson(Map<String, dynamic> json) {
    return NinoCercano(
      id: json['id'],
      nombre: json['nombre'],
      apellidoPaterno: json['apellido_paterno'] ?? '',
      apellidoMaterno: json['apellido_materno'] ?? '',
      nombreCompleto: json['nombre_completo'],
      posicion: PosicionCercana.fromJson(json['posicion']),
      distanciaMetros: (json['distancia_metros'] as num).toDouble(),
      distanciaKm: (json['distancia_km'] as num).toDouble(),
      ultimaActualizacion: json['ultima_actualizacion'],
      dentroAreaSegura: json['dentro_area_segura'],
      velocidadKmh: json['velocidad_kmh'] != null 
          ? (json['velocidad_kmh'] as num).toDouble() 
          : null,
      precisionMetros: json['precision_metros'] != null
          ? (json['precision_metros'] as num).toDouble()
          : null,
      kinder: KinderInfo.fromJson(json['kinder']),
      estado: json['estado'],
      estadoColor: json['estado_color'],
    );
  }

  String get distanciaFormateada {
    if (distanciaMetros < 1000) {
      return '${distanciaMetros.toStringAsFixed(0)} m';
    } else {
      return '${distanciaKm.toStringAsFixed(2)} km';
    }
  }

  String get velocidadFormateada {
    if (velocidadKmh == null) return '0 km/h';
    return '${velocidadKmh!.toStringAsFixed(1)} km/h';
  }

  String get precisionFormateada {
    if (precisionMetros == null) return 'N/A';
    return '±${precisionMetros!.toStringAsFixed(0)} m';
  }
}

class PosicionCercana {
  final double lat;
  final double lng;

  PosicionCercana({
    required this.lat,
    required this.lng,
  });

  factory PosicionCercana.fromJson(Map<String, dynamic> json) {
    return PosicionCercana(
      lat: (json['lat'] as num).toDouble(),
      lng: (json['lng'] as num).toDouble(),
    );
  }
}

class KinderInfo {
  final String? nombre;
  final String? direccion;

  KinderInfo({
    this.nombre,
    this.direccion,
  });

  factory KinderInfo.fromJson(Map<String, dynamic> json) {
    return KinderInfo(
      nombre: json['nombre'],
      direccion: json['direccion'],
    );
  }
}

class BusquedaCercanosResponse {
  final CentroBusqueda centroBusqueda;
  final int radioMetros;
  final int totalEncontrados;
  final List<NinoCercano> ninos;

  BusquedaCercanosResponse({
    required this.centroBusqueda,
    required this.radioMetros,
    required this.totalEncontrados,
    required this.ninos,
  });

  factory BusquedaCercanosResponse.fromJson(Map<String, dynamic> json) {
    return BusquedaCercanosResponse(
      centroBusqueda: CentroBusqueda.fromJson(json['centro_busqueda']),
      radioMetros: json['radio_metros'],
      totalEncontrados: json['total_encontrados'],
      ninos: (json['ninos'] as List)
          .map((item) => NinoCercano.fromJson(item))
          .toList(),
    );
  }
}

class CentroBusqueda {
  final double lat;
  final double lng;

  CentroBusqueda({
    required this.lat,
    required this.lng,
  });

  factory CentroBusqueda.fromJson(Map<String, dynamic> json) {
    return CentroBusqueda(
      lat: (json['lat'] as num).toDouble(),
      lng: (json['lng'] as num).toDouble(),
    );
  }
}
