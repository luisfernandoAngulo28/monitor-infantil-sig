import 'package:dio/dio.dart';
import '../config/api_config.dart';
import '../models/nino.dart';
import '../models/posicion_gps.dart';
import '../models/alerta.dart';
import 'auth_service.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  
  late final Dio _dio;
  late final AuthService _authService;
  
  ApiService._internal() {
    _dio = Dio(
      BaseOptions(
        baseUrl: ApiConfig.apiUrl,
        connectTimeout: ApiConfig.connectTimeout,
        receiveTimeout: ApiConfig.receiveTimeout,
      ),
    );
    _authService = AuthService();
    
    // Interceptor para agregar token automáticamente
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final token = await _authService.getAccessToken();
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          return handler.next(options);
        },
        onError: (error, handler) async {
          // Si es error 401, intentar refrescar token
          if (error.response?.statusCode == 401) {
            final refreshed = await _authService.refreshToken();
            if (refreshed) {
              // Reintentar la petición original
              final opts = error.requestOptions;
              final token = await _authService.getAccessToken();
              opts.headers['Authorization'] = 'Bearer $token';
              
              try {
                final response = await _dio.fetch(opts);
                return handler.resolve(response);
              } catch (e) {
                return handler.next(error);
              }
            }
          }
          return handler.next(error);
        },
      ),
    );
  }

  Future<List<Nino>> getMisNinos() async {
    try {
      final response = await _dio.get('${ApiConfig.configuracionUrl}mis_ninos/');
      final List<dynamic> data = response.data;
      return data.map((json) => Nino.fromJson(json)).toList();
    } catch (e) {
      print('Error al obtener niños: $e');
      rethrow;
    }
  }

  Future<EstadoNino> getEstadoNino(int ninoId) async {
    try {
      final response = await _dio.get('${ApiConfig.ninosUrl}$ninoId/estado/');
      return EstadoNino.fromJson(response.data);
    } catch (e) {
      print('Error al obtener estado del niño: $e');
      rethrow;
    }
  }

  Future<List<PosicionGPS>> getHistorialPosiciones(
    int ninoId, {
    int dias = 1,
  }) async {
    try {
      final response = await _dio.get(
        '${ApiConfig.ninosUrl}$ninoId/historial/',
        queryParameters: {'dias': dias},
      );
      
      final List<dynamic> features = response.data['features'];
      return features.map((json) => PosicionGPS.fromJson(json)).toList();
    } catch (e) {
      print('Error al obtener historial: $e');
      rethrow;
    }
  }

  Future<List<Alerta>> getMisAlertas() async {
    try {
      final response = await _dio.get(ApiConfig.misAlertasUrl);
      final List<dynamic> data = response.data;
      return data.map((json) => Alerta.fromJson(json)).toList();
    } catch (e) {
      print('Error al obtener alertas: $e');
      rethrow;
    }
  }

  Future<void> marcarAlertaLeida(int alertaId) async {
    try {
      await _dio.post('/alertas/$alertaId/marcar_leida/');
    } catch (e) {
      print('Error al marcar alerta como leída: $e');
      rethrow;
    }
  }

  Future<void> actualizarFirebaseToken(String token) async {
    try {
      await _dio.post(
        '${ApiConfig.configuracionUrl}actualizar_firebase_token/',
        data: {'firebase_token': token},
      );
    } catch (e) {
      print('Error al actualizar token Firebase: $e');
      rethrow;
    }
  }
}
