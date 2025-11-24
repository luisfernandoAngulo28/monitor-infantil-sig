# 📱 App Móvil Flutter - Monitor Infantil

## Vista Previa de la App

La app móvil permite a tutores/madres:
- 🗺️ Ver ubicación del niño en tiempo real
- ⚠️ Recibir alertas cuando sale del área
- 📊 Consultar historial de movimientos
- 🔔 Notificaciones push automáticas

---

## 🏗️ Estructura del Proyecto Flutter

```
monitor_infantil_app/
├── android/
├── ios/
├── lib/
│   ├── main.dart
│   ├── config/
│   │   └── api_config.dart           # URL del backend
│   ├── models/
│   │   ├── nino.dart
│   │   ├── posicion_gps.dart
│   │   ├── alerta.dart
│   │   └── centro_educativo.dart
│   ├── services/
│   │   ├── api_service.dart          # Cliente HTTP (Dio)
│   │   ├── auth_service.dart         # Login JWT
│   │   ├── tracking_service.dart     # Obtener estado/posiciones
│   │   └── notification_service.dart # Firebase Messaging
│   ├── providers/
│   │   ├── auth_provider.dart
│   │   ├── ninos_provider.dart
│   │   └── alertas_provider.dart
│   ├── screens/
│   │   ├── login_screen.dart
│   │   ├── home_screen.dart
│   │   ├── mapa_screen.dart          # Mapa con flutter_map
│   │   ├── alertas_screen.dart
│   │   └── historial_screen.dart
│   ├── widgets/
│   │   ├── mapa_widget.dart
│   │   ├── estado_nino_card.dart
│   │   └── alerta_dialog.dart
│   └── utils/
│       └── constants.dart
├── pubspec.yaml
└── README.md
```

---

## 📦 Dependencias (pubspec.yaml)

```yaml
name: monitor_infantil_app
description: App móvil para monitoreo de niños con SIG

dependencies:
  flutter:
    sdk: flutter
  
  # HTTP Client
  dio: ^5.4.0
  
  # Mapas
  flutter_map: ^6.0.0
  latlong2: ^0.9.0
  
  # Geolocalización (si simulas GPS)
  geolocator: ^10.1.0
  
  # Estado
  provider: ^6.1.0
  
  # Almacenamiento seguro (JWT)
  flutter_secure_storage: ^9.0.0
  
  # Notificaciones Push
  firebase_core: ^2.24.0
  firebase_messaging: ^14.7.0
  flutter_local_notifications: ^16.3.0
  
  # UI
  cupertino_icons: ^1.0.2
  intl: ^0.18.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
```

---

## 🔧 Configuración Inicial

### 1. Crear Proyecto Flutter

```bash
flutter create monitor_infantil_app
cd monitor_infantil_app
```

### 2. Agregar Dependencias

```bash
flutter pub add dio
flutter pub add flutter_map latlong2
flutter pub add provider
flutter pub add flutter_secure_storage
flutter pub add firebase_core firebase_messaging
flutter pub add flutter_local_notifications
flutter pub add geolocator
flutter pub add intl
```

### 3. Configurar Firebase (Opcional - para Push)

1. Ir a [Firebase Console](https://console.firebase.google.com/)
2. Crear proyecto "MonitorInfantil"
3. Agregar app Android
4. Descargar `google-services.json` → `android/app/`
5. Configurar en `android/build.gradle`

---

## 💻 Código Base

### config/api_config.dart

```dart
class ApiConfig {
  // Cambiar según tu entorno
  static const String baseUrl = 'http://10.0.2.2:8000'; // Android Emulator
  // static const String baseUrl = 'http://localhost:8000'; // iOS Simulator
  // static const String baseUrl = 'https://tu-backend.railway.app'; // Producción
  
  static const String apiUrl = '$baseUrl/api';
  
  // Endpoints
  static const String loginUrl = '$apiUrl/token/';
  static const String refreshUrl = '$apiUrl/token/refresh/';
  static const String ninosUrl = '$apiUrl/ninos/';
  static const String misAlertasUrl = '$apiUrl/mis-alertas/';
}
```

### services/auth_service.dart

```dart
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config/api_config.dart';

class AuthService {
  final Dio _dio = Dio();
  final FlutterSecureStorage _storage = FlutterSecureStorage();
  
  Future<bool> login(String username, String password) async {
    try {
      final response = await _dio.post(
        ApiConfig.loginUrl,
        data: {
          'username': username,
          'password': password,
        },
      );
      
      if (response.statusCode == 200) {
        // Guardar tokens
        await _storage.write(key: 'access_token', value: response.data['access']);
        await _storage.write(key: 'refresh_token', value: response.data['refresh']);
        return true;
      }
      return false;
    } catch (e) {
      print('Error login: $e');
      return false;
    }
  }
  
  Future<String?> getAccessToken() async {
    return await _storage.read(key: 'access_token');
  }
  
  Future<void> logout() async {
    await _storage.deleteAll();
  }
  
  Future<bool> isLoggedIn() async {
    final token = await getAccessToken();
    return token != null;
  }
}
```

### services/tracking_service.dart

```dart
import 'package:dio/dio.dart';
import '../config/api_config.dart';
import '../models/nino.dart';
import 'auth_service.dart';

class TrackingService {
  final Dio _dio = Dio();
  final AuthService _authService = AuthService();
  
  Future<Map<String, dynamic>> getEstadoNino(int ninoId) async {
    final token = await _authService.getAccessToken();
    
    final response = await _dio.get(
      '${ApiConfig.ninosUrl}$ninoId/estado/',
      options: Options(
        headers: {'Authorization': 'Bearer $token'},
      ),
    );
    
    return response.data;
  }
  
  Future<List<dynamic>> getMisNinos() async {
    final token = await _authService.getAccessToken();
    
    final response = await _dio.get(
      '${ApiConfig.apiUrl}/configuracion/mis_ninos/',
      options: Options(
        headers: {'Authorization': 'Bearer $token'},
      ),
    );
    
    return response.data;
  }
  
  Future<List<dynamic>> getMisAlertas() async {
    final token = await _authService.getAccessToken();
    
    final response = await _dio.get(
      ApiConfig.misAlertasUrl,
      options: Options(
        headers: {'Authorization': 'Bearer $token'},
      ),
    );
    
    return response.data;
  }
}
```

### screens/login_screen.dart

```dart
import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import 'home_screen.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final AuthService _authService = AuthService();
  bool _isLoading = false;
  
  Future<void> _login() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);
      
      final success = await _authService.login(
        _usernameController.text,
        _passwordController.text,
      );
      
      setState(() => _isLoading = false);
      
      if (success) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => HomeScreen()),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error de autenticación')),
        );
      }
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.child_care, size: 80, color: Colors.blue),
                SizedBox(height: 16),
                Text(
                  'Monitor Infantil SIG',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                SizedBox(height: 48),
                TextFormField(
                  controller: _usernameController,
                  decoration: InputDecoration(
                    labelText: 'Usuario',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.person),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Ingrese su usuario';
                    }
                    return null;
                  },
                ),
                SizedBox(height: 16),
                TextFormField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: InputDecoration(
                    labelText: 'Contraseña',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.lock),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Ingrese su contraseña';
                    }
                    return null;
                  },
                ),
                SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _login,
                    child: _isLoading
                        ? CircularProgressIndicator(color: Colors.white)
                        : Text('Ingresar', style: TextStyle(fontSize: 18)),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

### screens/home_screen.dart

```dart
import 'package:flutter/material.dart';
import '../services/tracking_service.dart';
import 'mapa_screen.dart';
import 'alertas_screen.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TrackingService _trackingService = TrackingService();
  List<dynamic> _ninos = [];
  bool _isLoading = true;
  
  @override
  void initState() {
    super.initState();
    _cargarNinos();
  }
  
  Future<void> _cargarNinos() async {
    try {
      final ninos = await _trackingService.getMisNinos();
      setState(() {
        _ninos = ninos;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error al cargar niños: $e')),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Monitor Infantil'),
        actions: [
          IconButton(
            icon: Icon(Icons.notifications),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => AlertasScreen()),
              );
            },
          ),
        ],
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _cargarNinos,
              child: ListView.builder(
                itemCount: _ninos.length,
                itemBuilder: (context, index) {
                  final nino = _ninos[index];
                  return Card(
                    margin: EdgeInsets.all(8),
                    child: ListTile(
                      leading: CircleAvatar(
                        child: Text(nino['nombre'][0]),
                      ),
                      title: Text(nino['nombre_completo']),
                      subtitle: Text(nino['centro_educativo']['nombre']),
                      trailing: Icon(Icons.arrow_forward_ios),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => MapaScreen(ninoId: nino['id']),
                          ),
                        );
                      },
                    ),
                  );
                },
              ),
            ),
    );
  }
}
```

### screens/mapa_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../services/tracking_service.dart';

class MapaScreen extends StatefulWidget {
  final int ninoId;
  
  MapaScreen({required this.ninoId});
  
  @override
  _MapaScreenState createState() => _MapaScreenState();
}

class _MapaScreenState extends State<MapaScreen> {
  final TrackingService _trackingService = TrackingService();
  Map<String, dynamic>? _estadoNino;
  bool _isLoading = true;
  
  @override
  void initState() {
    super.initState();
    _cargarEstado();
  }
  
  Future<void> _cargarEstado() async {
    try {
      final estado = await _trackingService.getEstadoNino(widget.ninoId);
      setState(() {
        _estadoNino = estado;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }
  
  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text('Mapa')),
        body: Center(child: CircularProgressIndicator()),
      );
    }
    
    final ultimaPosicion = _estadoNino?['ultima_posicion'];
    if (ultimaPosicion == null) {
      return Scaffold(
        appBar: AppBar(title: Text('Mapa')),
        body: Center(child: Text('No hay posición disponible')),
      );
    }
    
    final coords = ultimaPosicion['geometry']['coordinates'];
    final lat = coords[1];
    final lng = coords[0];
    final dentroArea = _estadoNino!['dentro_area_segura'] ?? true;
    
    return Scaffold(
      appBar: AppBar(
        title: Text(_estadoNino!['nino']['nombre_completo']),
        backgroundColor: dentroArea ? Colors.green : Colors.red,
      ),
      body: Column(
        children: [
          // Estado
          Container(
            color: dentroArea ? Colors.green : Colors.red,
            padding: EdgeInsets.all(16),
            child: Row(
              children: [
                Icon(
                  dentroArea ? Icons.check_circle : Icons.warning,
                  color: Colors.white,
                  size: 32,
                ),
                SizedBox(width: 16),
                Expanded(
                  child: Text(
                    dentroArea
                        ? '✅ Dentro del área segura'
                        : '⚠️ FUERA DEL ÁREA SEGURA',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ),
          // Mapa
          Expanded(
            child: FlutterMap(
              options: MapOptions(
                center: LatLng(lat, lng),
                zoom: 17,
              ),
              children: [
                TileLayer(
                  urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                ),
                MarkerLayer(
                  markers: [
                    Marker(
                      point: LatLng(lat, lng),
                      width: 40,
                      height: 40,
                      builder: (_) => Icon(
                        Icons.location_on,
                        color: dentroArea ? Colors.green : Colors.red,
                        size: 40,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _cargarEstado,
        child: Icon(Icons.refresh),
      ),
    );
  }
}
```

---

## 🚀 Comandos para Ejecutar

### Desarrollo

```bash
# Ejecutar en emulador Android
flutter run

# Ejecutar en dispositivo físico
flutter run -d <device_id>

# Hot reload durante desarrollo: presiona 'r'
```

### Build

```bash
# Build APK (Android)
flutter build apk --release

# Build App Bundle
flutter build appbundle

# Instalar en dispositivo
flutter install
```

---

## 🔗 Integración con Backend Django

### URL del Backend

**Desarrollo Local:**
- Android Emulator: `http://10.0.2.2:8000`
- iOS Simulator: `http://localhost:8000`
- Dispositivo físico: `http://TU_IP_LOCAL:8000`

**Producción:**
- Railway/Render: `https://tu-app.railway.app`

### Ejemplo de Consumo API

```dart
// Obtener estado del niño
final response = await dio.get(
  'http://10.0.2.2:8000/api/ninos/1/estado/',
  options: Options(
    headers: {'Authorization': 'Bearer $token'},
  ),
);

// Response:
{
  "nino": {...},
  "ultima_posicion": {
    "geometry": {"coordinates": [-63.1815, -17.7835]},
    "properties": {"dentro_area_segura": true}
  },
  "dentro_area_segura": true,
  "alertas_activas": 0
}
```

---

## 📱 Próximos Pasos

1. ✅ Crear proyecto Flutter
2. ✅ Configurar dependencias
3. ✅ Implementar login con JWT
4. ✅ Consumir API de niños
5. ✅ Mostrar mapa con posición
6. ⏳ Configurar Firebase (notificaciones push)
7. ⏳ Implementar pantalla de alertas
8. ⏳ Agregar historial de posiciones

¿Necesitas ayuda con alguna pantalla específica de la app? 📱
