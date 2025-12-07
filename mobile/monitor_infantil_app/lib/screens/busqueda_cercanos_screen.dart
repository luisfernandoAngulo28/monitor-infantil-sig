import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:geolocator/geolocator.dart';
import 'dart:async';
import '../models/nino_cercano.dart';
import '../services/api_service.dart';

class BusquedaCercanosScreen extends StatefulWidget {
  const BusquedaCercanosScreen({Key? key}) : super(key: key);

  @override
  State<BusquedaCercanosScreen> createState() => _BusquedaCercanosScreenState();
}

class _BusquedaCercanosScreenState extends State<BusquedaCercanosScreen> {
  GoogleMapController? _mapController;
  final ApiService _apiService = ApiService();
  
  Position? _currentPosition;
  BusquedaCercanosResponse? _resultadoBusqueda;
  Set<Marker> _markers = {};
  Set<Circle> _circles = {};
  
  bool _isLoading = false;
  bool _locationPermissionGranted = false;
  double _radiusBusqueda = 5000; // metros
  
  final List<double> _radiusOptions = [500, 1000, 2000, 5000, 10000, 20000];

  @override
  void initState() {
    super.initState();
    _checkLocationPermission();
  }

  Future<void> _checkLocationPermission() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      _showError('Los servicios de ubicación están desactivados');
      return;
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        _showError('Permiso de ubicación denegado');
        return;
      }
    }

    if (permission == LocationPermission.deniedForever) {
      _showError('Permiso de ubicación denegado permanentemente');
      return;
    }

    setState(() {
      _locationPermissionGranted = true;
    });

    await _getCurrentLocation();
  }

  Future<void> _getCurrentLocation() async {
    if (!_locationPermissionGranted) return;

    setState(() {
      _isLoading = true;
    });

    try {
      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );

      setState(() {
        _currentPosition = position;
      });

      // Mover cámara a ubicación actual
      if (_mapController != null) {
        _mapController!.animateCamera(
          CameraUpdate.newLatLngZoom(
            LatLng(position.latitude, position.longitude),
            14,
          ),
        );
      }

      // Buscar niños cercanos automáticamente
      await _buscarNinosCercanos();
    } catch (e) {
      _showError('Error al obtener ubicación: $e');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _buscarNinosCercanos() async {
    if (_currentPosition == null) {
      _showError('Primero obtén tu ubicación actual');
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      final resultado = await _apiService.buscarNinosCercanos(
        lat: _currentPosition!.latitude,
        lng: _currentPosition!.longitude,
        radiusMetros: _radiusBusqueda.toInt(),
      );

      setState(() {
        _resultadoBusqueda = resultado;
      });

      _actualizarMarcadores();
      
      if (resultado.totalEncontrados == 0) {
        _showInfo('No se encontraron niños en un radio de ${_formatearDistancia(_radiusBusqueda)}');
      } else {
        _showSuccess('Se encontraron ${resultado.totalEncontrados} niño(s) cercano(s)');
      }
    } catch (e) {
      _showError('Error al buscar niños cercanos: $e');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _actualizarMarcadores() {
    if (_resultadoBusqueda == null || _currentPosition == null) return;

    final Set<Marker> newMarkers = {};
    final Set<Circle> newCircles = {};

    // Marcador de mi ubicación
    newMarkers.add(
      Marker(
        markerId: const MarkerId('mi_ubicacion'),
        position: LatLng(_currentPosition!.latitude, _currentPosition!.longitude),
        icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueBlue),
        infoWindow: const InfoWindow(
          title: '📍 Mi ubicación',
          snippet: 'Centro de búsqueda',
        ),
      ),
    );

    // Círculo de radio de búsqueda
    newCircles.add(
      Circle(
        circleId: const CircleId('radio_busqueda'),
        center: LatLng(_currentPosition!.latitude, _currentPosition!.longitude),
        radius: _radiusBusqueda,
        fillColor: Colors.blue.withOpacity(0.1),
        strokeColor: Colors.blue,
        strokeWidth: 2,
      ),
    );

    // Marcadores de niños encontrados
    for (var nino in _resultadoBusqueda!.ninos) {
      final color = nino.dentroAreaSegura 
          ? BitmapDescriptor.hueGreen 
          : BitmapDescriptor.hueRed;

      newMarkers.add(
        Marker(
          markerId: MarkerId('nino_${nino.id}'),
          position: LatLng(nino.posicion.lat, nino.posicion.lng),
          icon: BitmapDescriptor.defaultMarkerWithHue(color),
          infoWindow: InfoWindow(
            title: nino.nombreCompleto,
            snippet: '${nino.distanciaFormateada} - ${nino.estado}',
          ),
          onTap: () => _mostrarDetallesNino(nino),
        ),
      );
    }

    setState(() {
      _markers = newMarkers;
      _circles = newCircles;
    });
  }

  void _mostrarDetallesNino(NinoCercano nino) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.6,
        minChildSize: 0.4,
        maxChildSize: 0.9,
        expand: false,
        builder: (context, scrollController) => SingleChildScrollView(
          controller: scrollController,
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header con nombre
                Row(
                  children: [
                    Container(
                      width: 10,
                      height: 10,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: nino.dentroAreaSegura ? Colors.green : Colors.red,
                      ),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        nino.nombreCompleto,
                        style: const TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                
                // Estado
                _buildInfoCard(
                  icon: Icons.info_outline,
                  title: 'Estado',
                  value: nino.estado,
                  color: nino.dentroAreaSegura ? Colors.green : Colors.red,
                ),
                const SizedBox(height: 12),
                
                // Distancia
                _buildInfoCard(
                  icon: Icons.location_on,
                  title: 'Distancia',
                  value: nino.distanciaFormateada,
                  color: Colors.blue,
                ),
                const SizedBox(height: 12),
                
                // Velocidad
                if (nino.velocidadKmh != null)
                  _buildInfoCard(
                    icon: Icons.speed,
                    title: 'Velocidad',
                    value: nino.velocidadFormateada,
                    color: Colors.orange,
                  ),
                const SizedBox(height: 12),
                
                // Precisión GPS
                if (nino.precisionMetros != null)
                  _buildInfoCard(
                    icon: Icons.gps_fixed,
                    title: 'Precisión GPS',
                    value: nino.precisionFormateada,
                    color: Colors.purple,
                  ),
                const SizedBox(height: 12),
                
                // Kinder
                _buildInfoCard(
                  icon: Icons.school,
                  title: 'Kinder',
                  value: nino.kinder.nombre ?? 'N/A',
                  subtitle: nino.kinder.direccion,
                  color: Colors.teal,
                ),
                const SizedBox(height: 12),
                
                // Última actualización
                if (nino.ultimaActualizacion != null)
                  _buildInfoCard(
                    icon: Icons.access_time,
                    title: 'Última actualización',
                    value: _formatearFecha(nino.ultimaActualizacion!),
                    color: Colors.grey,
                  ),
                const SizedBox(height: 20),
                
                // Botón para navegar
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: () {
                      // Centrar mapa en el niño
                      _mapController?.animateCamera(
                        CameraUpdate.newLatLngZoom(
                          LatLng(nino.posicion.lat, nino.posicion.lng),
                          16,
                        ),
                      );
                      Navigator.pop(context);
                    },
                    icon: const Icon(Icons.navigation),
                    label: const Text('Ver en mapa'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildInfoCard({
    required IconData icon,
    required String title,
    required String value,
    String? subtitle,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Row(
        children: [
          Icon(icon, color: color, size: 32),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[600],
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  value,
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: color,
                  ),
                ),
                if (subtitle != null) ...[
                  const SizedBox(height: 4),
                  Text(
                    subtitle,
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  String _formatearDistancia(double metros) {
    if (metros < 1000) {
      return '${metros.toInt()} m';
    } else {
      return '${(metros / 1000).toStringAsFixed(1)} km';
    }
  }

  String _formatearFecha(String isoDate) {
    try {
      final fecha = DateTime.parse(isoDate);
      final ahora = DateTime.now();
      final diferencia = ahora.difference(fecha);

      if (diferencia.inMinutes < 1) {
        return 'Hace unos segundos';
      } else if (diferencia.inMinutes < 60) {
        return 'Hace ${diferencia.inMinutes} min';
      } else if (diferencia.inHours < 24) {
        return 'Hace ${diferencia.inHours} h';
      } else {
        return 'Hace ${diferencia.inDays} día(s)';
      }
    } catch (e) {
      return isoDate;
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.error_outline, color: Colors.white),
            const SizedBox(width: 10),
            Expanded(child: Text(message)),
          ],
        ),
        backgroundColor: Colors.red,
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  void _showInfo(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.info_outline, color: Colors.white),
            const SizedBox(width: 10),
            Expanded(child: Text(message)),
          ],
        ),
        backgroundColor: Colors.orange,
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  void _showSuccess(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.check_circle_outline, color: Colors.white),
            const SizedBox(width: 10),
            Expanded(child: Text(message)),
          ],
        ),
        backgroundColor: Colors.green,
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  void _mostrarListadoNinos() {
    if (_resultadoBusqueda == null || _resultadoBusqueda!.ninos.isEmpty) {
      _showInfo('No hay niños para mostrar');
      return;
    }

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        minChildSize: 0.5,
        maxChildSize: 0.95,
        expand: false,
        builder: (context, scrollController) => Column(
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.blue.shade50,
                borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Niños cercanos (${_resultadoBusqueda!.totalEncontrados})',
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
            ),
            
            // Lista
            Expanded(
              child: ListView.builder(
                controller: scrollController,
                padding: const EdgeInsets.all(16),
                itemCount: _resultadoBusqueda!.ninos.length,
                itemBuilder: (context, index) {
                  final nino = _resultadoBusqueda!.ninos[index];
                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    elevation: 2,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                      side: BorderSide(
                        color: nino.dentroAreaSegura 
                            ? Colors.green.withOpacity(0.3)
                            : Colors.red.withOpacity(0.3),
                        width: 2,
                      ),
                    ),
                    child: ListTile(
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 8,
                      ),
                      leading: CircleAvatar(
                        backgroundColor: nino.dentroAreaSegura 
                            ? Colors.green 
                            : Colors.red,
                        child: Text(
                          nino.nombre[0].toUpperCase(),
                          style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      title: Text(
                        nino.nombreCompleto,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                        ),
                      ),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const SizedBox(height: 4),
                          Row(
                            children: [
                              Icon(Icons.location_on, size: 16, color: Colors.grey[600]),
                              const SizedBox(width: 4),
                              Text(nino.distanciaFormateada),
                            ],
                          ),
                          const SizedBox(height: 2),
                          Text(
                            nino.kinder.nombre ?? '',
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey[600],
                            ),
                          ),
                        ],
                      ),
                      trailing: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 4,
                            ),
                            decoration: BoxDecoration(
                              color: nino.dentroAreaSegura 
                                  ? Colors.green.withOpacity(0.2)
                                  : Colors.red.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              nino.dentroAreaSegura ? 'Seguro' : 'Fuera',
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                                color: nino.dentroAreaSegura 
                                    ? Colors.green.shade700
                                    : Colors.red.shade700,
                              ),
                            ),
                          ),
                        ],
                      ),
                      onTap: () {
                        Navigator.pop(context);
                        _mostrarDetallesNino(nino);
                      },
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Búsqueda de Niños Cercanos'),
        actions: [
          // Mostrar listado
          if (_resultadoBusqueda != null && _resultadoBusqueda!.ninos.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.list),
              onPressed: _mostrarListadoNinos,
              tooltip: 'Ver listado',
            ),
          
          // Selector de radio
          PopupMenuButton<double>(
            icon: const Icon(Icons.tune),
            tooltip: 'Radio de búsqueda',
            onSelected: (value) {
              setState(() {
                _radiusBusqueda = value;
              });
              _buscarNinosCercanos();
            },
            itemBuilder: (context) => _radiusOptions.map((radius) {
              return PopupMenuItem<double>(
                value: radius,
                child: Row(
                  children: [
                    if (radius == _radiusBusqueda)
                      const Icon(Icons.check, color: Colors.blue)
                    else
                      const SizedBox(width: 24),
                    const SizedBox(width: 8),
                    Text(_formatearDistancia(radius)),
                  ],
                ),
              );
            }).toList(),
          ),
        ],
      ),
      body: Stack(
        children: [
          // Mapa
          _currentPosition == null
              ? const Center(
                  child: CircularProgressIndicator(),
                )
              : GoogleMap(
                  initialCameraPosition: CameraPosition(
                    target: LatLng(
                      _currentPosition!.latitude,
                      _currentPosition!.longitude,
                    ),
                    zoom: 14,
                  ),
                  onMapCreated: (controller) {
                    _mapController = controller;
                  },
                  markers: _markers,
                  circles: _circles,
                  myLocationEnabled: true,
                  myLocationButtonEnabled: false,
                  compassEnabled: true,
                  mapToolbarEnabled: false,
                  zoomControlsEnabled: false,
                ),

          // Loading overlay
          if (_isLoading)
            Container(
              color: Colors.black26,
              child: const Center(
                child: Card(
                  child: Padding(
                    padding: EdgeInsets.all(20.0),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        CircularProgressIndicator(),
                        SizedBox(height: 16),
                        Text('Buscando niños cercanos...'),
                      ],
                    ),
                  ),
                ),
              ),
            ),

          // Info panel superior
          if (_resultadoBusqueda != null)
            Positioned(
              top: 16,
              left: 16,
              right: 16,
              child: Card(
                elevation: 4,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      Column(
                        children: [
                          const Icon(Icons.group, color: Colors.blue),
                          const SizedBox(height: 4),
                          Text(
                            '${_resultadoBusqueda!.totalEncontrados}',
                            style: const TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const Text(
                            'Encontrados',
                            style: TextStyle(fontSize: 12, color: Colors.grey),
                          ),
                        ],
                      ),
                      Container(
                        width: 1,
                        height: 40,
                        color: Colors.grey[300],
                      ),
                      Column(
                        children: [
                          const Icon(Icons.radar, color: Colors.orange),
                          const SizedBox(height: 4),
                          Text(
                            _formatearDistancia(_radiusBusqueda),
                            style: const TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const Text(
                            'Radio',
                            style: TextStyle(fontSize: 12, color: Colors.grey),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          // Botón mi ubicación
          FloatingActionButton(
            heroTag: 'my_location',
            onPressed: _getCurrentLocation,
            tooltip: 'Mi ubicación',
            child: const Icon(Icons.my_location),
          ),
          const SizedBox(height: 16),
          
          // Botón buscar
          FloatingActionButton.extended(
            heroTag: 'search',
            onPressed: _buscarNinosCercanos,
            icon: const Icon(Icons.search),
            label: const Text('Buscar'),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _mapController?.dispose();
    super.dispose();
  }
}
