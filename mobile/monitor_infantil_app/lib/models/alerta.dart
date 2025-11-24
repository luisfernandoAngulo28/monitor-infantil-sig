class Alerta {
  final int id;
  final String tipoAlerta;
  final String tipoAlertaDisplay;
  final String estado;
  final String estadoDisplay;
  final String mensaje;
  final DateTime fechaCreacion;
  final DateTime? fechaEnviada;
  final DateTime? fechaLeida;
  final String ninoNombre;

  Alerta({
    required this.id,
    required this.tipoAlerta,
    required this.tipoAlertaDisplay,
    required this.estado,
    required this.estadoDisplay,
    required this.mensaje,
    required this.fechaCreacion,
    this.fechaEnviada,
    this.fechaLeida,
    required this.ninoNombre,
  });

  factory Alerta.fromJson(Map<String, dynamic> json) {
    return Alerta(
      id: json['id'],
      tipoAlerta: json['tipo_alerta'],
      tipoAlertaDisplay: _getTipoAlertaDisplay(json['tipo_alerta']),
      estado: json['estado'],
      estadoDisplay: _getEstadoDisplay(json['estado']),
      mensaje: json['mensaje'],
      fechaCreacion: DateTime.parse(json['fecha_creacion']),
      fechaEnviada: json['fecha_enviada'] != null
          ? DateTime.parse(json['fecha_enviada'])
          : null,
      fechaLeida: json['fecha_leida'] != null
          ? DateTime.parse(json['fecha_leida'])
          : null,
      ninoNombre: json['nino']['nombre_completo'],
    );
  }

  static String _getTipoAlertaDisplay(String tipo) {
    switch (tipo) {
      case 'SALIDA_AREA':
        return 'Salida del Área';
      case 'BATERIA_BAJA':
        return 'Batería Baja';
      case 'SIN_SEÑAL':
        return 'Sin Señal GPS';
      case 'MANUAL':
        return 'Alerta Manual';
      default:
        return tipo;
    }
  }

  static String _getEstadoDisplay(String estado) {
    switch (estado) {
      case 'PENDIENTE':
        return 'Pendiente';
      case 'ENVIADA':
        return 'Enviada';
      case 'LEIDA':
        return 'Leída';
      case 'RESUELTA':
        return 'Resuelta';
      default:
        return estado;
    }
  }

  bool get esNoLeida => estado == 'PENDIENTE' || estado == 'ENVIADA';
}
