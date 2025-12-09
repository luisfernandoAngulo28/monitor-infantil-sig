class ApiConfig {
  // Configuración del backend
  // Cambiar según tu entorno
  
  // PRODUCCIÓN - DigitalOcean con HTTPS
  // static const String baseUrl = 'https://monitor-infantil.duckdns.org';
  
  // PRODUCCIÓN - IP directa (sin SSL)
  // static const String baseUrl = 'http://143.198.30.170:8000';
  
  // Android Emulator (desarrollo local) - Usar 10.0.2.2 para acceder a localhost
  // static const String baseUrl = 'http://10.0.2.2:8000';
  
  // Android Emulator con Docker - Usar IP de red local
  // static const String baseUrl = 'http://10.80.243.77:8000';
  
  // Linux Desktop / Chrome (desarrollo local)
  // static const String baseUrl = 'http://localhost:8000';
  
  // iOS Simulator (descomentar si usas iOS)
  // static const String baseUrl = 'http://localhost:8000';
  
  // Dispositivo físico en la misma red (cambiar IP)
  static const String baseUrl = 'http://10.80.243.77:8000';
  
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
