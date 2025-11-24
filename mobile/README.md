# 📱 Mobile App - Monitor Infantil SIG

Aplicación móvil Flutter para tutores/madres que permite monitorear la ubicación de niños en tiempo real.

## 📋 Descripción

La app móvil permite a los tutores:
- 🗺️ Ver ubicación del niño en tiempo real en el mapa
- ⚠️ Recibir alertas push cuando el niño sale del área segura
- 📊 Consultar historial de movimientos
- 🔔 Gestionar notificaciones

## 🚀 Inicio Rápido

### Requisitos Previos
- Flutter SDK 3.x
- Android Studio / Xcode
- Dart 3.x

### Instalación

```bash
# 1. Crear proyecto Flutter
flutter create monitor_infantil_app
cd monitor_infantil_app

# 2. Agregar dependencias
flutter pub add dio
flutter pub add flutter_map latlong2
flutter pub add provider
flutter pub add flutter_secure_storage
flutter pub add firebase_core firebase_messaging
flutter pub add flutter_local_notifications
flutter pub add geolocator

# 3. Configurar Firebase (opcional - para push notifications)
# - Descargar google-services.json de Firebase Console
# - Colocar en android/app/

# 4. Ejecutar app
flutter run
```

## 📦 Dependencias Principales

```yaml
dependencies:
  # HTTP Client
  dio: ^5.4.0
  
  # Mapas
  flutter_map: ^6.0.0
  latlong2: ^0.9.0
  
  # Estado
  provider: ^6.1.0
  
  # Almacenamiento seguro (JWT)
  flutter_secure_storage: ^9.0.0
  
  # Push Notifications
  firebase_core: ^2.24.0
  firebase_messaging: ^14.7.0
  flutter_local_notifications: ^16.3.0
  
  # GPS
  geolocator: ^10.1.0
```

## 🏗️ Estructura del Proyecto

```
monitor_infantil_app/
├── lib/
│   ├── main.dart
│   ├── config/
│   │   └── api_config.dart
│   ├── models/
│   │   ├── nino.dart
│   │   ├── posicion_gps.dart
│   │   └── alerta.dart
│   ├── services/
│   │   ├── api_service.dart
│   │   ├── auth_service.dart
│   │   ├── tracking_service.dart
│   │   └── notification_service.dart
│   ├── providers/
│   │   ├── auth_provider.dart
│   │   └── ninos_provider.dart
│   ├── screens/
│   │   ├── login_screen.dart
│   │   ├── home_screen.dart
│   │   ├── mapa_screen.dart
│   │   └── alertas_screen.dart
│   └── widgets/
│       ├── mapa_widget.dart
│       └── estado_nino_card.dart
├── android/
├── ios/
└── pubspec.yaml
```

## 🔧 Configuración

### Backend API URL

Editar `lib/config/api_config.dart`:

```dart
class ApiConfig {
  // Desarrollo
  static const String baseUrl = 'http://10.0.2.2:8000'; // Android Emulator
  // static const String baseUrl = 'http://localhost:8000'; // iOS
  
  // Producción
  // static const String baseUrl = 'https://tu-backend.com';
}
```

### Firebase (Notificaciones Push)

1. Crear proyecto en [Firebase Console](https://console.firebase.google.com/)
2. Agregar app Android/iOS
3. Descargar `google-services.json` → `android/app/`
4. Descargar `GoogleService-Info.plist` → `ios/Runner/`

## 📱 Pantallas

### 1. Login
- Autenticación con JWT
- Almacenamiento seguro de tokens

### 2. Home
- Lista de niños del tutor
- Estado actual (dentro/fuera del área)
- Acceso rápido al mapa

### 3. Mapa
- Visualización con flutter_map
- Polígono del área del kinder
- Marcador GPS del niño (verde/rojo)
- Estado en tiempo real
- Auto-refresh

### 4. Alertas
- Lista de alertas históricas
- Marcar como leída
- Detalles de cada alerta

## 🔔 Notificaciones Push

La app recibe notificaciones automáticas cuando:
- El niño sale del área segura
- Batería baja del dispositivo
- Sin señal GPS prolongada

```dart
// Ejemplo de manejo de notificación
FirebaseMessaging.onMessage.listen((RemoteMessage message) {
  showDialog(
    context: context,
    builder: (_) => AlertDialog(
      title: Text('⚠️ ALERTA'),
      content: Text(message.notification?.body ?? ''),
    ),
  );
});
```

## 🧪 Comandos Útiles

```bash
# Ejecutar en debug mode
flutter run

# Build APK (Android)
flutter build apk --release

# Build App Bundle
flutter build appbundle

# Ejecutar tests
flutter test

# Limpiar cache
flutter clean

# Obtener dependencias
flutter pub get
```

## 🌐 API Consumida

La app consume el backend Django en `../backend/`:

**Endpoints principales:**
- `POST /api/token/` - Login
- `GET /api/ninos/` - Listar niños
- `GET /api/ninos/{id}/estado/` - Estado actual
- `GET /api/mis-alertas/` - Alertas del tutor
- `POST /api/configuracion/actualizar_firebase_token/` - Registrar token FCM

## 📖 Documentación

Ver documentación completa:
- [Guía Flutter App](../SIG22/docs/FLUTTER_APP.md)
- [Documentación API](../backend/apps/api/API_DOCS.md)

## 🚀 Despliegue

### Android
```bash
flutter build apk --release
# APK en: build/app/outputs/flutter-apk/app-release.apk
```

### iOS
```bash
flutter build ios --release
# Abrir en Xcode para firmar y publicar
```

## 🎨 Diseño

Colores del tema:
- **Primario**: Azul #007bff (áreas seguras)
- **Éxito**: Verde #28a745 (dentro del área)
- **Peligro**: Rojo #dc3545 (fuera del área)
- **Advertencia**: Amarillo #ffc107 (alertas)

## 📝 TODO

- [ ] Implementar login screen
- [ ] Consumir API de niños
- [ ] Mostrar mapa con flutter_map
- [ ] Configurar Firebase
- [ ] Implementar notificaciones push
- [ ] Agregar pantalla de alertas
- [ ] Tests unitarios
- [ ] Tests de integración

## 🆘 Soporte

Para dudas sobre Flutter, consultar:
- [Flutter Documentation](https://docs.flutter.dev/)
- [Dart Packages](https://pub.dev/)
- Documentación del proyecto en `../SIG22/docs/`
