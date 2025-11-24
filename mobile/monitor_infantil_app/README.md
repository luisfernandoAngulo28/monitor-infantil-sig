# Monitor Infantil - App Móvil Flutter

Aplicación móvil para el monitoreo geográfico de niños prescolares.

## ✅ Estado del Proyecto

**Proyecto completado y listo para ejecutar.**

### Archivos Creados

#### 📁 Configuración
- ✅ `lib/config/api_config.dart` - Configuración de URLs del backend

#### 📁 Modelos
- ✅ `lib/models/nino.dart` - Modelo de Niño y CentroEducativo
- ✅ `lib/models/posicion_gps.dart` - Modelo de PosicionGPS y EstadoNino
- ✅ `lib/models/alerta.dart` - Modelo de Alertas

#### 📁 Servicios
- ✅ `lib/services/auth_service.dart` - Autenticación JWT
- ✅ `lib/services/api_service.dart` - Cliente API con interceptores

#### 📁 Providers (State Management)
- ✅ `lib/providers/auth_provider.dart` - Estado de autenticación
- ✅ `lib/providers/ninos_provider.dart` - Estado de niños y posiciones

#### 📁 Pantallas
- ✅ `lib/screens/login_screen.dart` - Pantalla de inicio de sesión
- ✅ `lib/screens/home_screen.dart` - Pantalla principal con navegación
- ✅ `lib/screens/mapa_screen.dart` - Mapa con ubicación en tiempo real
- ✅ `lib/screens/alertas_screen.dart` - Lista de alertas

#### 📁 Main
- ✅ `lib/main.dart` - Punto de entrada con providers y navegación

### Dependencias Instaladas

```yaml
dependencies:
  dio: ^5.7.0                           # Cliente HTTP
  flutter_map: ^7.0.2                   # Mapas OpenStreetMap
  latlong2: ^0.9.1                      # Coordenadas geográficas
  provider: ^6.1.2                      # State management
  flutter_secure_storage: ^9.2.2       # Almacenamiento seguro (tokens)
  geolocator: ^13.0.2                   # Geolocalización
  intl: ^0.20.1                         # Formateo de fechas
```

## 🚀 Configuración Inicial

### 1. Configurar Backend URL

Editar `lib/config/api_config.dart`:

```dart
// Para Android Emulator
static const String baseUrl = 'http://10.0.2.2:8000';

// Para iOS Simulator
// static const String baseUrl = 'http://localhost:8000';

// Para dispositivo físico en la misma red WiFi
// static const String baseUrl = 'http://192.168.1.100:8000';  // Tu IP local
```

### 2. Verificar Backend

Asegúrate de que el backend Django esté corriendo:

```bash
cd ../backend
python manage.py runserver
```

Verifica que puedas acceder a: `http://localhost:8000/api/`

### 3. Ejecutar la App

#### Android Emulator

```bash
# Listar emuladores disponibles
flutter emulators

# Abrir emulador (ejemplo)
flutter emulators --launch Pixel_7_API_34

# Ejecutar app
flutter run
```

#### Dispositivo Físico Android

1. Activar **Modo Desarrollador** en el dispositivo
2. Activar **Depuración USB**
3. Conectar el dispositivo por USB
4. Cambiar la URL en `api_config.dart` a tu IP local
5. Ejecutar:

```bash
flutter run
```

#### iOS Simulator (solo en macOS)

```bash
# Abrir simulador
open -a Simulator

# Ejecutar app
flutter run
```

## 📱 Funcionalidades

### 1. Login
- Autenticación con JWT
- Almacenamiento seguro de tokens
- Validación de formularios

### 2. Mapa
- Visualización de ubicación del niño en OpenStreetMap
- Selector de niño (si tienes múltiples)
- Indicador de estado (dentro/fuera del área segura)
- Indicador de batería

### 3. Alertas
- Lista de alertas en tiempo real
- Marcado de alertas como leídas
- Pull-to-refresh
- Filtros visuales por tipo de alerta

## 🔐 Usuarios de Prueba

Usar los mismos usuarios creados en el backend:

```
Usuario: tutor1
Contraseña: demo123456
```

## 🛠️ Comandos Útiles

### Verificar dispositivos conectados
```bash
flutter devices
```

### Limpiar proyecto
```bash
flutter clean
flutter pub get
```

### Verificar problemas
```bash
flutter doctor
```

### Actualizar dependencias
```bash
flutter pub upgrade
```

### Ver logs en tiempo real
```bash
flutter logs
```

## 📂 Estructura del Proyecto

```
lib/
├── config/
│   └── api_config.dart          # URLs y configuración del backend
├── models/
│   ├── alerta.dart              # Modelo de alertas
│   ├── nino.dart                # Modelo de niño
│   └── posicion_gps.dart        # Modelo de posiciones GPS
├── providers/
│   ├── auth_provider.dart       # Estado de autenticación
│   └── ninos_provider.dart      # Estado de niños y ubicaciones
├── screens/
│   ├── alertas_screen.dart      # Pantalla de alertas
│   ├── home_screen.dart         # Pantalla principal
│   ├── login_screen.dart        # Pantalla de login
│   └── mapa_screen.dart         # Pantalla de mapa
├── services/
│   ├── api_service.dart         # Cliente API REST
│   └── auth_service.dart        # Servicio de autenticación
└── main.dart                    # Punto de entrada
```

## 🔧 Personalización

### Cambiar el tema de la app

Editar `lib/main.dart`:

```dart
theme: ThemeData(
  primarySwatch: Colors.green,  // Cambiar color principal
  useMaterial3: true,
),
```

### Agregar íconos personalizados

1. Agregar imágenes en `assets/images/`
2. Actualizar `pubspec.yaml`:

```yaml
flutter:
  assets:
    - assets/images/
```

### Configurar Firebase (Notificaciones Push)

1. Crear proyecto en [Firebase Console](https://console.firebase.google.com/)
2. Descargar `google-services.json` (Android) y `GoogleService-Info.plist` (iOS)
3. Instalar dependencias:

```bash
flutter pub add firebase_core firebase_messaging
```

4. Seguir la [guía oficial de Firebase](https://firebase.google.com/docs/flutter/setup)

## 🐛 Solución de Problemas

### Error: "Unable to connect to API"

1. Verificar que el backend esté corriendo
2. Verificar la URL en `api_config.dart`
3. Para Android Emulator, usar `http://10.0.2.2:8000`
4. Para dispositivo físico, usar la IP local

### Error: "Gradle build failed" (Android)

```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
flutter run
```

### Error: "CocoaPods" (iOS)

```bash
cd ios
pod install
cd ..
flutter run
```

### La app se cierra al abrir

Verificar logs:

```bash
flutter logs
```

## 📊 Próximas Mejoras

- [ ] Notificaciones push con Firebase Cloud Messaging
- [ ] Historial de ubicaciones en el mapa
- [ ] Modo offline con caché local
- [ ] Perfil del niño con fotos
- [ ] Configuración de intervalos de actualización
- [ ] Modo oscuro
- [ ] Internacionalización (i18n)

## 📄 Licencia

Proyecto académico - INF442 Sistemas de Información Geográfica
