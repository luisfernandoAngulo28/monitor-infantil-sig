import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';

class FirebaseService {
  static final FirebaseService _instance = FirebaseService._internal();
  factory FirebaseService() => _instance;
  FirebaseService._internal();

  final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;
  final FlutterLocalNotificationsPlugin _localNotifications =
      FlutterLocalNotificationsPlugin();
  static const String _fcmTokenKey = 'fcm_token';

  // Inicializar Firebase Messaging
  Future<void> initialize() async {
    // Solicitar permisos
    NotificationSettings settings = await _firebaseMessaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      provisional: false,
    );

    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      print('Usuario autorizó las notificaciones');
      
      // Obtener token FCM
      String? token = await _firebaseMessaging.getToken();
      if (token != null) {
        print('FCM Token: $token');
        // Guardar token localmente para enviarlo después del login
        await _saveTokenLocally(token);
      }

      // Configurar notificaciones locales
      await _initializeLocalNotifications();

      // Escuchar mensajes en primer plano
      FirebaseMessaging.onMessage.listen(_handleForegroundMessage);

      // Manejar cuando se toca una notificación
      FirebaseMessaging.onMessageOpenedApp.listen(_handleMessageOpenedApp);

      // Verificar si la app se abrió desde una notificación
      RemoteMessage? initialMessage =
          await _firebaseMessaging.getInitialMessage();
      if (initialMessage != null) {
        _handleMessageOpenedApp(initialMessage);
      }

      // Escuchar actualizaciones del token
      _firebaseMessaging.onTokenRefresh.listen((newToken) {
        print('Token actualizado: $newToken');
        _saveTokenLocally(newToken);
      });
    } else {
      print('Usuario denegó las notificaciones');
    }
  }

  // Guardar token FCM localmente
  Future<void> _saveTokenLocally(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_fcmTokenKey, token);
  }

  // Enviar token FCM guardado al backend (después del login)
  Future<void> sendTokenToBackend() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString(_fcmTokenKey);
      if (token != null) {
        await ApiService().actualizarFirebaseToken(token);
        print('Token FCM enviado al backend correctamente');
      }
    } catch (e) {
      print('Error al enviar token al backend: $e');
    }
  }

  // Configurar notificaciones locales
  Future<void> _initializeLocalNotifications() async {
    const AndroidInitializationSettings androidSettings =
        AndroidInitializationSettings('@mipmap/ic_launcher');

    const DarwinInitializationSettings iosSettings =
        DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );

    const InitializationSettings initSettings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );

    await _localNotifications.initialize(
      initSettings,
      onDidReceiveNotificationResponse: _onNotificationTapped,
    );
  }

  // Manejar mensajes en primer plano
  void _handleForegroundMessage(RemoteMessage message) {
    print('Mensaje recibido en primer plano: ${message.messageId}');

    RemoteNotification? notification = message.notification;
    AndroidNotification? android = message.notification?.android;

    if (notification != null && android != null) {
      _showLocalNotification(
        title: notification.title ?? 'Monitor Infantil',
        body: notification.body ?? '',
        payload: message.data.toString(),
      );
    }
  }

  // Manejar cuando se abre la app desde una notificación
  void _handleMessageOpenedApp(RemoteMessage message) {
    print('Notificación tocada: ${message.data}');
    // Aquí puedes navegar a una pantalla específica
    // Por ejemplo, a la pantalla de alertas
  }

  // Mostrar notificación local
  Future<void> _showLocalNotification({
    required String title,
    required String body,
    String? payload,
  }) async {
    const AndroidNotificationDetails androidDetails =
        AndroidNotificationDetails(
      'alertas_channel',
      'Alertas de Niños',
      channelDescription: 'Notificaciones cuando un niño sale del área segura',
      importance: Importance.max,
      priority: Priority.high,
      showWhen: true,
      icon: '@mipmap/ic_launcher',
    );

    const DarwinNotificationDetails iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );

    const NotificationDetails platformDetails = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _localNotifications.show(
      DateTime.now().millisecondsSinceEpoch ~/ 1000,
      title,
      body,
      platformDetails,
      payload: payload,
    );
  }

  // Manejar cuando se toca una notificación local
  void _onNotificationTapped(NotificationResponse response) {
    print('Notificación local tocada: ${response.payload}');
    // Navegar a la pantalla correspondiente
  }

  // Obtener el token FCM actual
  Future<String?> getToken() async {
    return await _firebaseMessaging.getToken();
  }

  // Cancelar todas las notificaciones
  Future<void> cancelAllNotifications() async {
    await _localNotifications.cancelAll();
  }
}

// Manejador para mensajes en segundo plano (debe estar en nivel superior)
@pragma('vm:entry-point')
Future<void> firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  print('Mensaje recibido en segundo plano: ${message.messageId}');
}
