import 'dart:async';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';
import '../models/alerta.dart';

class AlertasScreen extends StatefulWidget {
  const AlertasScreen({super.key});

  @override
  State<AlertasScreen> createState() => _AlertasScreenState();
}

class _AlertasScreenState extends State<AlertasScreen> {
  final ApiService _apiService = ApiService();
  List<Alerta> _alertas = [];
  bool _isLoading = false;
  String? _error;
  Timer? _refreshTimer;

  @override
  void initState() {
    super.initState();
    _cargarAlertas();
    // Actualizar cada 10 segundos
    _refreshTimer = Timer.periodic(const Duration(seconds: 10), (timer) {
      _cargarAlertas();
    });
  }

  @override
  void dispose() {
    _refreshTimer?.cancel();
    super.dispose();
  }

  Future<void> _cargarAlertas() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      print('📋 Cargando alertas...');
      final alertas = await _apiService.getMisAlertas();
      print('✅ Alertas cargadas: ${alertas.length}');
      setState(() {
        _alertas = alertas;
        _isLoading = false;
      });
    } catch (e) {
      print('❌ Error al cargar alertas: $e');
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  Future<void> _marcarLeida(Alerta alerta) async {
    try {
      await _apiService.marcarAlertaLeida(alerta.id);
      _cargarAlertas(); // Recargar alertas
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Alerta marcada como leída')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Color _getColorPorTipo(String tipo) {
    switch (tipo) {
      case 'SALIDA_AREA':
        return Colors.red;
      case 'BATERIA_BAJA':
        return Colors.orange;
      case 'SIN_SEÑAL':
        return Colors.grey;
      default:
        return Colors.blue;
    }
  }

  IconData _getIconoPorTipo(String tipo) {
    switch (tipo) {
      case 'SALIDA_AREA':
        return Icons.warning;
      case 'BATERIA_BAJA':
        return Icons.battery_alert;
      case 'SIN_SEÑAL':
        return Icons.signal_wifi_off;
      default:
        return Icons.info;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_error != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 48, color: Colors.red),
            const SizedBox(height: 16),
            Text('Error: $_error'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _cargarAlertas,
              child: const Text('Reintentar'),
            ),
          ],
        ),
      );
    }

    if (_alertas.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.notifications_off, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text(
              'No hay alertas',
              style: TextStyle(fontSize: 18, color: Colors.grey),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _cargarAlertas,
      child: ListView.builder(
        itemCount: _alertas.length,
        itemBuilder: (context, index) {
          final alerta = _alertas[index];
          final color = _getColorPorTipo(alerta.tipoAlerta);
          final icono = _getIconoPorTipo(alerta.tipoAlerta);

          return Card(
            margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            color: alerta.esNoLeida ? color.withOpacity(0.1) : null,
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: color,
                child: Icon(icono, color: Colors.white),
              ),
              title: Text(
                alerta.ninoNombre,
                style: TextStyle(
                  fontWeight: alerta.esNoLeida ? FontWeight.bold : FontWeight.normal,
                ),
              ),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(alerta.mensaje),
                  const SizedBox(height: 4),
                  Text(
                    DateFormat('dd/MM/yyyy HH:mm').format(alerta.fechaCreacion),
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
              trailing: alerta.esNoLeida
                  ? IconButton(
                      icon: const Icon(Icons.mark_email_read),
                      onPressed: () => _marcarLeida(alerta),
                      tooltip: 'Marcar como leída',
                    )
                  : Icon(
                      Icons.check_circle,
                      color: Colors.grey[400],
                    ),
              isThreeLine: true,
            ),
          );
        },
      ),
    );
  }
}
