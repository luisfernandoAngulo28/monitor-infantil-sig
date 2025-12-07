import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'dart:convert';
import '../config/api_config.dart';

class AuthService {
  final Dio _dio = Dio(
    BaseOptions(
      connectTimeout: ApiConfig.connectTimeout,
      receiveTimeout: ApiConfig.receiveTimeout,
      // Removido validateStatus para que use el comportamiento por defecto
      // (solo acepta 200-299 como válidos)
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
        // JWT Authentication devuelve: {"access": "xxx", "refresh": "yyy"}
        final accessToken = response.data['access'] as String?;
        final refreshToken = response.data['refresh'] as String?;
        
        if (accessToken == null) {
          print('❌ Access token es null en la respuesta');
          return false;
        }
        
        print('✅ Access token recibido: ${accessToken.substring(0, 10)}...');
        
        await _storage.write(
          key: 'access_token',
          value: accessToken,
        );
        
        if (refreshToken != null) {
          await _storage.write(
            key: 'refresh_token',
            value: refreshToken,
          );
        }
        
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

  Future<String?> getToken() async {
    return await getAccessToken();
  }

  Future<int?> getTutorId() async {
    try {
      final token = await getAccessToken();
      if (token == null) return null;

      // Decodificar JWT (formato: header.payload.signature)
      final parts = token.split('.');
      if (parts.length != 3) return null;

      // Decodificar el payload (parte central)
      final payload = parts[1];
      final normalized = base64Url.normalize(payload);
      final decoded = utf8.decode(base64Url.decode(normalized));
      final Map<String, dynamic> payloadMap = json.decode(decoded);

      // El JWT contiene user_id que puede ser String o int
      final userId = payloadMap['user_id'];
      if (userId is int) {
        return userId;
      } else if (userId is String) {
        return int.tryParse(userId);
      }
      return null;
    } catch (e) {
      print('❌ Error decodificando JWT: $e');
      return null;
    }
  }
}
