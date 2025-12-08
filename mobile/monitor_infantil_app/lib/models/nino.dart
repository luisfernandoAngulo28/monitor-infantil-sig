class Nino {
  final int id;
  final String? nombre;
  final String? apellidoPaterno;
  final String? apellidoMaterno;
  final String? nombreCompleto;
  final String? fechaNacimiento;
  final int? edad;
  final String? sexo;
  final String? foto;
  final CentroEducativo? centroEducativo;
  final bool trackingActivo;
  final bool activo;

  Nino({
    required this.id,
    this.nombre,
    this.apellidoPaterno,
    this.apellidoMaterno,
    this.nombreCompleto,
    this.fechaNacimiento,
    this.edad,
    this.sexo,
    this.foto,
    this.centroEducativo,
    required this.trackingActivo,
    required this.activo,
  });

  factory Nino.fromJson(Map<String, dynamic> json) {
    return Nino(
      id: json['id'],
      nombre: json['nombre'],
      apellidoPaterno: json['apellido_paterno'],
      apellidoMaterno: json['apellido_materno'],
      nombreCompleto: json['nombre_completo'],
      fechaNacimiento: json['fecha_nacimiento'],
      edad: json['edad'],
      sexo: json['sexo'],
      foto: json['foto'],
      centroEducativo: json['centro_educativo'] != null 
          ? CentroEducativo.fromJson(json['centro_educativo'])
          : null,
      trackingActivo: json['tracking_activo'],
      activo: json['activo'],
    );
  }
}

class CentroEducativo {
  final int id;
  final String? nombre;
  final String? codigo;
  final String? direccion;
  final String? telefono;

  CentroEducativo({
    required this.id,
    this.nombre,
    this.codigo,
    this.direccion,
    this.telefono,
  });

  factory CentroEducativo.fromJson(Map<String, dynamic> json) {
    return CentroEducativo(
      id: json['id'],
      nombre: json['nombre'],
      codigo: json['codigo'],
      direccion: json['direccion'],
      telefono: json['telefono'],
    );
  }
}
