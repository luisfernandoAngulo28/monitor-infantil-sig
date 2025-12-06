import 'package:flutter/material.dart';
import '../services/auth_service.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService = AuthService();
  
  bool _isAuthenticated = false;
  bool _isLoading = false;
  int? _tutorId;
  String? _token;

  bool get isAuthenticated => _isAuthenticated;
  bool get isLoading => _isLoading;
  int? get tutorId => _tutorId;
  String? get token => _token;

  Future<void> checkAuthStatus() async {
    _isLoading = true;
    notifyListeners();

    _isAuthenticated = await _authService.isLoggedIn();
    
    // Si está autenticado, cargar tutorId y token
    if (_isAuthenticated) {
      _tutorId = await _authService.getTutorId();
      _token = await _authService.getToken();
    } else {
      _tutorId = null;
      _token = null;
    }
    
    _isLoading = false;
    notifyListeners();
  }

  Future<bool> login(String username, String password) async {
    _isLoading = true;
    notifyListeners();

    final success = await _authService.login(username, password);
    
    if (success) {
      _isAuthenticated = true;
      // Obtener tutorId y token del servicio
      _tutorId = await _authService.getTutorId();
      _token = await _authService.getToken();
    }
    
    _isLoading = false;
    notifyListeners();
    
    return success;
  }

  Future<void> logout() async {
    await _authService.logout();
    _isAuthenticated = false;
    _tutorId = null;
    _token = null;
    notifyListeners();
  }
}
