import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:provider/provider.dart';
import '../providers/gps_tracking_provider.dart';
import '../providers/auth_provider.dart';
import '../config/api_config.dart';

/// Ejemplo de pantalla de mapa con WebSocket GPS en tiempo real.
/// 
/// Esta pantalla muestra:
/// - Mapa con posiciones de niños actualizadas en tiempo real
/// - Indicador de conexión WebSocket
/// - Alertas cuando niños salen del área
class MapaRealTimeScreen extends StatefulWidget {
  const MapaRealTimeScreen({Key? key}) : super(key: key);

  @override
  State<MapaRealTimeScreen> createState() => _MapaRealTimeScreenState();
}

class _MapaRealTimeScreenState extends State<MapaRealTimeScreen> {
  GoogleMapController? _mapController;
  
  // Posición inicial (Santa Cruz, Bolivia)
  static const LatLng _initialPosition = LatLng(-17.7833, -63.1812);

  @override
  void initState() {
    super.initState();
    // Conectar WebSocket después de que el widget esté construido
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _connectWebSocket();
    });
  }

  void _connectWebSocket() {
    // Conectar al WebSocket cuando se carga la pantalla
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final gpsProvider = Provider.of<GPSTrackingProvider>(context, listen: false);

    debugPrint('🔍 Verificando autenticación...');
    debugPrint('  isAuthenticated: ${authProvider.isAuthenticated}');
    debugPrint('  tutorId: ${authProvider.tutorId}');
    debugPrint('  token: ${authProvider.token != null ? "presente" : "null"}');

    // Solo conectar si el usuario está autenticado
    if (authProvider.isAuthenticated && authProvider.tutorId != null && authProvider.token != null) {
      gpsProvider.connect(
        serverUrl: ApiConfig.baseUrl, // Usar configuración del entorno
        tutorId: authProvider.tutorId!,
        authToken: authProvider.token,
      );

      debugPrint('🔌 WebSocket conectado para tutor ${authProvider.tutorId}');
    } else {
      debugPrint('⚠️ No se puede conectar WebSocket: usuario no autenticado o datos incompletos');
      
      // Mostrar mensaje al usuario
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Debe iniciar sesión para ver el tracking en tiempo real'),
              backgroundColor: Colors.orange,
            ),
          );
        }
      });
    }
  }

  @override
  void dispose() {
    // Desconectar WebSocket al salir de la pantalla
    final gpsProvider = Provider.of<GPSTrackingProvider>(context, listen: false);
    gpsProvider.disconnect();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tracking en Tiempo Real'),
        actions: [
          // Indicador de conexión WebSocket
          Consumer<GPSTrackingProvider>(
            builder: (context, gpsProvider, child) {
              return Padding(
                padding: const EdgeInsets.all(8.0),
                child: Row(
                  children: [
                    Icon(
                      gpsProvider.isConnected 
                          ? Icons.wifi 
                          : Icons.wifi_off,
                      color: gpsProvider.isConnected 
                          ? Colors.green 
                          : Colors.red,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      gpsProvider.isConnected ? 'En línea' : 'Desconectado',
                      style: TextStyle(
                        fontSize: 12,
                        color: gpsProvider.isConnected 
                            ? Colors.green 
                            : Colors.red,
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ],
      ),
      body: Stack(
        children: [
          // Mapa con marcadores actualizados en tiempo real
          Consumer<GPSTrackingProvider>(
            builder: (context, gpsProvider, child) {
              // Convertir posiciones a marcadores
              final markers = _buildMarkers(gpsProvider);

              return GoogleMap(
                initialCameraPosition: const CameraPosition(
                  target: _initialPosition,
                  zoom: 15,
                ),
                onMapCreated: (controller) {
                  _mapController = controller;
                },
                markers: markers,
                myLocationEnabled: true,
                myLocationButtonEnabled: true,
                zoomControlsEnabled: true,
              );
            },
          ),

          // Panel de alertas (si hay)
          Consumer<GPSTrackingProvider>(
            builder: (context, gpsProvider, child) {
              if (gpsProvider.recentAlerts.isEmpty) {
                return const SizedBox.shrink();
              }

              return Positioned(
                top: 0,
                left: 0,
                right: 0,
                child: _buildAlertsPanel(gpsProvider),
              );
            },
          ),

          // Botón para centrar en el primer niño
          Positioned(
            bottom: 80,
            right: 16,
            child: FloatingActionButton(
              heroTag: 'center_map',
              onPressed: _centerMapOnFirstChild,
              child: const Icon(Icons.my_location),
            ),
          ),

          // Botón para solicitar marcadores de prueba
          Positioned(
            bottom: 150,
            right: 16,
            child: FloatingActionButton(
              heroTag: 'test_markers',
              backgroundColor: Colors.orange,
              onPressed: () {
                final gpsProvider = Provider.of<GPSTrackingProvider>(context, listen: false);
                gpsProvider.requestTestMarkers();
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Solicitando marcadores de prueba...')),
                );
              },
              child: const Icon(Icons.bug_report),
            ),
          ),
        ],
      ),
    );
  }

  /// Construir marcadores desde las posiciones GPS
  Set<Marker> _buildMarkers(GPSTrackingProvider gpsProvider) {
    return gpsProvider.latestPositions.entries.map((entry) {
      final ninoId = entry.key;
      final posicion = entry.value;

      return Marker(
        markerId: MarkerId('nino_$ninoId'),
        position: LatLng(
          posicion.ubicacion.latitude,
          posicion.ubicacion.longitude,
        ),
        icon: posicion.dentroAreaSegura
            ? BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueGreen)
            : BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueRed),
        infoWindow: InfoWindow(
          title: 'Niño $ninoId',
          snippet: _buildMarkerSnippet(posicion),
        ),
        onTap: () => _onMarkerTapped(ninoId, posicion),
      );
    }).toSet();
  }

  String _buildMarkerSnippet(posicion) {
    final status = posicion.dentroAreaSegura 
        ? '✅ En área segura' 
        : '⚠️ Fuera del área';
    final battery = '🔋 ${posicion.nivelBateria}%';
    return '$status\n$battery';
  }

  /// Panel de alertas recientes
  Widget _buildAlertsPanel(GPSTrackingProvider gpsProvider) {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.red.shade100,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              const Icon(Icons.warning, color: Colors.red),
              const SizedBox(width: 8),
              const Text(
                'Alertas Recientes',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.red,
                ),
              ),
              const Spacer(),
              IconButton(
                icon: const Icon(Icons.close, color: Colors.red),
                onPressed: () {
                  gpsProvider.clearAlerts();
                },
              ),
            ],
          ),
          const SizedBox(height: 8),
          ...gpsProvider.recentAlerts.take(3).map((alerta) {
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: Text(
                alerta,
                style: TextStyle(
                  color: Colors.red.shade900,
                  fontSize: 14,
                ),
              ),
            );
          }),
        ],
      ),
    );
  }

  /// Centrar mapa en el primer niño
  void _centerMapOnFirstChild() {
    final gpsProvider = Provider.of<GPSTrackingProvider>(context, listen: false);
    
    if (gpsProvider.latestPositions.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('No hay posiciones GPS disponibles')),
      );
      return;
    }

    final firstPosition = gpsProvider.latestPositions.values.first;
    _mapController?.animateCamera(
      CameraUpdate.newLatLngZoom(
        LatLng(
          firstPosition.ubicacion.latitude,
          firstPosition.ubicacion.longitude,
        ),
        16,
      ),
    );
  }

  /// Cuando se toca un marcador
  void _onMarkerTapped(int ninoId, posicion) {
    debugPrint('📍 Marcador tocado - Niño $ninoId');
    
    // Aquí puedes mostrar un bottom sheet con más detalles
    showModalBottomSheet(
      context: context,
      builder: (context) => _buildNinoDetailsSheet(ninoId, posicion),
    );
  }

  /// Bottom sheet con detalles del niño
  Widget _buildNinoDetailsSheet(int ninoId, posicion) {
    return Container(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Niño $ninoId',
            style: const TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 16),
          
          _buildDetailRow(
            Icons.location_on,
            'Ubicación',
            '${posicion.ubicacion.latitude.toStringAsFixed(6)}, ${posicion.ubicacion.longitude.toStringAsFixed(6)}',
          ),
          
          _buildDetailRow(
            Icons.check_circle,
            'Estado',
            posicion.dentroAreaSegura ? 'En área segura' : 'Fuera del área',
            color: posicion.dentroAreaSegura ? Colors.green : Colors.red,
          ),
          
          _buildDetailRow(
            Icons.battery_full,
            'Batería',
            '${posicion.nivelBateria}%',
            color: posicion.nivelBateria < 20 ? Colors.red : Colors.green,
          ),
          
          _buildDetailRow(
            Icons.access_time,
            'Última actualización',
            _formatTimestamp(posicion.timestamp),
          ),
          
          const SizedBox(height: 16),
          
          ElevatedButton.icon(
            onPressed: () {
              Navigator.pop(context);
              // Aquí puedes navegar a una pantalla de detalles
            },
            icon: const Icon(Icons.info),
            label: const Text('Ver más detalles'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size(double.infinity, 48),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDetailRow(IconData icon, String label, String value, {Color? color}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Icon(icon, size: 20, color: color ?? Colors.grey),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: const TextStyle(
                    fontSize: 12,
                    color: Colors.grey,
                  ),
                ),
                Text(
                  value,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                    color: color,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final diff = now.difference(timestamp);

    if (diff.inSeconds < 60) {
      return 'Hace ${diff.inSeconds} segundos';
    } else if (diff.inMinutes < 60) {
      return 'Hace ${diff.inMinutes} minutos';
    } else {
      return 'Hace ${diff.inHours} horas';
    }
  }
}
