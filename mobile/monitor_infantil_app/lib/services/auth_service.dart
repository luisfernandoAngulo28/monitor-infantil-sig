import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config/api_config.dart';

class AuthService {
  final Dio _dio = Dio(
    BaseOptions(
      connectTimeout: ApiConfig.connectTimeout,
      receiveTimeout: ApiConfig.receiveTimeout,
      validateStatus: (status) => status! < 500, // Aceptar todos los códigos < 500
    ),
  );
  
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  Future<bool> login(String username, String password) async {
    try {
      print('🔐 Intentando login en: ${ApiConfig.loginUrl}');
      print('📝 Usuario: $username');
      
      final response = await _dio.post(
        ApiConfig.loginUrl,
        data: {
          'username': username,
          'password': password,
        },
        options: Options(
          headers: {
            'Content-Type': 'application/json',
          },
        ),
      );

      print('📡 Response status: ${response.statusCode}');
      print('📦 Response data: ${response.data}');

      if (response.statusCode == 200) {
        // Django Rest Framework Token Authentication devuelve: {"token": "xxx"}
        final token = response.data['token'] as String?;
        
        if (token == null) {
          print('❌ Token es null en la respuesta');
          return false;
        }
        
        print('✅ Token recibido: ${token.substring(0, 10)}...');
        
        await _storage.write(
          key: 'access_token',
          value: token,
        );
        return true;
      }
      
      print('❌ Status code no es 200: ${response.statusCode}');
      return false;
    } catch (e) {
      print('❌ Error en login: $e');
      if (e is DioException) {
        print('   Status: ${e.response?.statusCode}');
        print('   Data: ${e.response?.data}');
        print('   Message: ${e.message}');
      }
      return false;
    }
  }

  Future<String?> getAccessToken() async {
    return await _storage.read(key: 'access_token');
  }

  Future<String?> getRefreshToken() async {
    return await _storage.read(key: 'refresh_token');
  }

  Future<bool> refreshToken() async {
    try {
      final refreshToken = await getRefreshToken();
      if (refreshToken == null) return false;

      final response = await _dio.post(
        ApiConfig.refreshUrl,
        data: {'refresh': refreshToken},
      );

      if (response.statusCode == 200) {
        await _storage.write(
          key: 'access_token',
          value: response.data['access'],
        );
        return true;
      }
      return false;
    } catch (e) {
      print('Error al refrescar token: $e');
      return false;
    }
  }

  Future<void> logout() async {
    await _storage.deleteAll();
  }

  Future<bool> isLoggedIn() async {
    final token = await getAccessToken();
    return token != null;
  }
}
