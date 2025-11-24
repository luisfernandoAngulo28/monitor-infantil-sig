import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/nino.dart';
import '../models/posicion_gps.dart';

class NinosProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  List<Nino> _ninos = [];
  Map<int, EstadoNino> _estados = {};
  bool _isLoading = false;
  String? _error;

  List<Nino> get ninos => _ninos;
  Map<int, EstadoNino> get estados => _estados;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> cargarNinos() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _ninos = await _apiService.getMisNinos();
      
      // Cargar estado de cada niño
      for (var nino in _ninos) {
        try {
          final estado = await _apiService.getEstadoNino(nino.id);
          _estados[nino.id] = estado;
        } catch (e) {
          print('Error al cargar estado del niño ${nino.id}: $e');
        }
      }
      
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> actualizarEstado(int ninoId) async {
    try {
      final estado = await _apiService.getEstadoNino(ninoId);
      _estados[ninoId] = estado;
      notifyListeners();
    } catch (e) {
      print('Error al actualizar estado: $e');
    }
  }

  EstadoNino? getEstado(int ninoId) {
    return _estados[ninoId];
  }
}
