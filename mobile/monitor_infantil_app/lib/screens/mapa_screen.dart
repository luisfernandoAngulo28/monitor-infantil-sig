import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:provider/provider.dart';
import '../providers/ninos_provider.dart';
import '../models/nino.dart';

class MapaScreen extends StatefulWidget {
  const MapaScreen({super.key});

  @override
  State<MapaScreen> createState() => _MapaScreenState();
}

class _MapaScreenState extends State<MapaScreen> {
  final MapController _mapController = MapController();
  Nino? _ninoSeleccionado;

  @override
  Widget build(BuildContext context) {
    return Consumer<NinosProvider>(
      builder: (context, ninosProvider, child) {
        if (ninosProvider.isLoading) {
          return const Center(child: CircularProgressIndicator());
        }

        if (ninosProvider.error != null) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, size: 48, color: Colors.red),
                const SizedBox(height: 16),
                Text('Error: ${ninosProvider.error}'),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () => ninosProvider.cargarNinos(),
                  child: const Text('Reintentar'),
                ),
              ],
            ),
          );
        }

        if (ninosProvider.ninos.isEmpty) {
          return const Center(
            child: Text('No hay niños registrados'),
          );
        }

        // Si no hay niño seleccionado, seleccionar el primero
        if (_ninoSeleccionado == null || 
            !ninosProvider.ninos.any((n) => n.id == _ninoSeleccionado?.id)) {
          _ninoSeleccionado = ninosProvider.ninos.first;
        }

        final estado = ninosProvider.getEstado(_ninoSeleccionado!.id);
        final ultimaPosicion = estado?.ultimaPosicion;

        return Column(
          children: [
            // Selector de niño
            Container(
              color: Colors.grey[200],
              padding: const EdgeInsets.all(8.0),
              child: Row(
                children: [
                  const Icon(Icons.child_care),
                  const SizedBox(width: 8),
                  Expanded(
                    child: DropdownButton<Nino>(
                      isExpanded: true,
                      value: _ninoSeleccionado,
                      hint: const Text('Selecciona un niño'),
                      items: ninosProvider.ninos.map((nino) {
                        return DropdownMenuItem<Nino>(
                          value: nino,
                          child: Text(nino.nombreCompleto ?? '${nino.nombre} ${nino.apellidoPaterno}'),
                        );
                      }).toList(),
                      onChanged: (nino) {
                        setState(() {
                          _ninoSeleccionado = nino;
                        });
                        if (nino != null) {
                          ninosProvider.actualizarEstado(nino.id);
                        }
                      },
                    ),
                  ),
                ],
              ),
            ),

            // Estado del niño
            if (estado != null)
              Container(
                color: estado.dentroAreaSegura ? Colors.green[100] : Colors.red[100],
                padding: const EdgeInsets.all(12.0),
                child: Row(
                  children: [
                    Icon(
                      estado.dentroAreaSegura
                          ? Icons.check_circle
                          : Icons.warning,
                      color: estado.dentroAreaSegura ? Colors.green : Colors.red,
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        estado.dentroAreaSegura
                            ? 'En área segura'
                            : '¡FUERA DEL ÁREA SEGURA!',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: estado.dentroAreaSegura ? Colors.green[900] : Colors.red[900],
                        ),
                      ),
                    ),
                    if (estado.nivelBateria != null)
                      Row(
                        children: [
                          Icon(
                            Icons.battery_std,
                            size: 20,
                            color: estado.nivelBateria! < 20
                                ? Colors.red
                                : Colors.grey[700],
                          ),
                          Text('${estado.nivelBateria}%'),
                        ],
                      ),
                  ],
                ),
              ),

            // Mapa
            Expanded(
              child: ultimaPosicion != null
                  ? FlutterMap(
                      mapController: _mapController,
                      options: MapOptions(
                        initialCenter: ultimaPosicion.ubicacion,
                        initialZoom: 16.0,
                      ),
                      children: [
                        TileLayer(
                          urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                          userAgentPackageName: 'com.example.monitor_infantil',
                        ),
                        
                        // Marcador de posición
                        MarkerLayer(
                          markers: [
                            Marker(
                              point: ultimaPosicion.ubicacion,
                              width: 40,
                              height: 40,
                              child: Icon(
                                Icons.person_pin_circle,
                                size: 40,
                                color: estado?.dentroAreaSegura == true
                                    ? Colors.green
                                    : Colors.red,
                              ),
                            ),
                          ],
                        ),
                      ],
                    )
                  : const Center(
                      child: Text('No hay ubicación disponible'),
                    ),
            ),
          ],
        );
      },
    );
  }
}
