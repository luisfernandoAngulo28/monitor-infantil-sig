class ApiConfig {
  // Configuración del backend
  // Cambiar según tu entorno
  
  // Android Emulator
  static const String baseUrl = 'http://10.0.2.2:8000';
  
  // iOS Simulator (descomentar si usas iOS)
  // static const String baseUrl = 'http://localhost:8000';
  
  // Dispositivo físico en la misma red (cambiar IP)
  // static const String baseUrl = 'http://192.168.1.100:8000';
  
  // Producción
  // static const String baseUrl = 'https://tu-backend.railway.app';
  
  static const String apiUrl = '$baseUrl/api';
  
  // Endpoints
  static const String loginUrl = '$apiUrl/token/';
  static const String refreshUrl = '$apiUrl/token/refresh/';
  static const String ninosUrl = '$apiUrl/ninos/';
  static const String centrosUrl = '$apiUrl/centros/';
  static const String misAlertasUrl = '$apiUrl/mis-alertas/';
  static const String configuracionUrl = '$apiUrl/configuracion/';
  
  // Timeout
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
}
