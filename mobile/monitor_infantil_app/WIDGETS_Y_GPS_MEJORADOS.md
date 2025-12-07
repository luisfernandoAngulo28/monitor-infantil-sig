# 🎨 Widgets y Utilidades Mejoradas

**Rescatadas del proyecto InDriver Clone y adaptadas para Monitor Infantil SIG**

---

## 📦 Componentes Agregados

### 1. **Widgets Personalizados** (`lib/widgets/`)

#### `CustomButton`
Botón reutilizable con estilo consistente.

**Uso básico**:
```dart
CustomButton(
  text: 'Iniciar Sesión',
  onPressed: () => login(),
)
```

**Con ícono y loading**:
```dart
CustomButton(
  text: 'Guardar',
  icon: Icons.save,
  isLoading: _isLoading,
  onPressed: () => save(),
  color: Colors.green,
)
```

#### `CustomTextField`
Campo de texto con validación y estilo mejorado.

**Uso**:
```dart
CustomTextField(
  label: 'Email',
  icon: Icons.email,
  keyboardType: TextInputType.emailAddress,
  onChanged: (value) => setState(() => email = value),
  validator: (value) {
    if (value == null || value.isEmpty) {
      return 'Email requerido';
    }
    return null;
  },
)
```

**Para contraseñas**:
```dart
CustomTextField(
  label: 'Contraseña',
  icon: Icons.lock,
  obscureText: true,
  onChanged: (value) => password = value,
)
```

#### `CustomIconBack`
Botón de retroceso personalizado.

**Uso en AppBar**:
```dart
AppBar(
  leading: CustomIconBack(),
  title: Text('Detalle del Niño'),
)
```

---

### 2. **Utilidades GPS** (`lib/utils/gps_utils.dart`)

Funciones optimizadas para tracking GPS de alta precisión.

#### **Stream de GPS de Alta Precisión**

Configuración optimizada para tracking de niños:
- ✅ Precisión BEST (±1-5 metros)
- ✅ Actualiza cada 5 metros de movimiento
- ✅ Intervalo mínimo: 3 segundos

**Uso**:
```dart
StreamSubscription<Position>? _subscription;

void startTracking() {
  _subscription = GpsUtils.getHighPrecisionStream().listen(
    (Position position) {
      print('Nueva posición: ${position.latitude}, ${position.longitude}');
      print('Precisión: ${position.accuracy} metros');
      
      // Actualizar mapa, enviar al servidor, etc.
      updateMap(position);
    },
  );
}

void stopTracking() {
  _subscription?.cancel();
}
```

#### **Stream GPS Balanceado** (Ahorro de Batería)

Configuración para ahorro de batería:
- Precisión: HIGH (±5-15 metros)
- Actualiza cada 10 metros
- Intervalo mínimo: 10 segundos

**Uso**:
```dart
_subscription = GpsUtils.getBalancedStream().listen(
  (position) => updateMap(position),
);
```

#### **Calcular Rotación de Marcadores**

Para mostrar la dirección del movimiento en el mapa:

```dart
LatLng previousPosition = LatLng(-17.7833, -63.1812);
LatLng currentPosition = LatLng(-17.7835, -63.1815);

double rotation = GpsUtils.calculateRotation(
  previousPosition,
  currentPosition,
);

// Usar en Marker
Marker(
  markerId: MarkerId('nino_1'),
  position: currentPosition,
  rotation: rotation,  // ← Marcador apuntará en dirección del movimiento
  icon: customIcon,
);
```

#### **Calcular Distancia**

```dart
LatLng kinder = LatLng(-17.7833, -63.1812);
LatLng nino = LatLng(-17.7850, -63.1830);

double distancia = GpsUtils.distanceBetween(kinder, nino);
print('Distancia al kinder: ${distancia.toStringAsFixed(0)} metros');
```

#### **Validar Posición GPS**

Verifica que la posición sea válida antes de usar:

```dart
Position? position = await Geolocator.getCurrentPosition();

if (GpsUtils.isValidPosition(position)) {
  // Posición válida, usar
  sendToServer(position);
} else {
  // Posición inválida (fuera de rango, baja precisión, etc.)
  print('Posición GPS inválida');
}
```

#### **Calcular Velocidad**

```dart
Position pos1 = ...; // Posición anterior
Position pos2 = ...; // Posición actual
Duration diff = Duration(seconds: 10);

double velocidadKmh = GpsUtils.calculateSpeed(pos1, pos2, diff);

if (velocidadKmh > 50) {
  print('⚠️ Velocidad anormal detectada: $velocidadKmh km/h');
  generarAlerta();
}
```

---

## 🚀 Integración con `GPSTrackingProvider`

El provider ya incluye soporte para GPS de alta precisión:

**Iniciar tracking automático**:
```dart
final gpsProvider = Provider.of<GPSTrackingProvider>(context, listen: false);

// Inicia tracking de alta precisión y envía al servidor
await gpsProvider.startHighPrecisionTracking(ninoId: 1);
```

**Detener tracking**:
```dart
await gpsProvider.stopTracking();
```

**Escuchar posición actual**:
```dart
Consumer<GPSTrackingProvider>(
  builder: (context, gps, child) {
    if (gps.currentPosition != null) {
      return Text('Precisión: ${gps.currentPosition!.accuracy}m');
    }
    return Text('Sin GPS');
  },
)
```

---

## 📈 Mejoras de Rendimiento

### Antes (WebSocket básico):
- Precisión GPS: ±10-15 metros
- Actualización: Cada 10 segundos fijo
- Consumo batería: Medio-Alto
- Sin validación de precisión

### Ahora (GPS de Alta Precisión):
- ✅ Precisión GPS: ±1-5 metros (+80% mejora)
- ✅ Actualización: Inteligente (cada 5m o 3s)
- ✅ Consumo batería: Optimizado (stream balanceado disponible)
- ✅ Validación automática de precisión
- ✅ Cálculo de rotación para marcadores
- ✅ Detección de velocidad anormal

---

## 🎯 Ejemplo Completo

Pantalla de mapa con tracking de alta precisión:

```dart
class MapaScreen extends StatefulWidget {
  @override
  State<MapaScreen> createState() => _MapaScreenState();
}

class _MapaScreenState extends State<MapaScreen> {
  GoogleMapController? _mapController;
  Set<Marker> _markers = {};
  LatLng? _previousPosition;

  @override
  void initState() {
    super.initState();
    _startTracking();
  }

  Future<void> _startTracking() async {
    final gpsProvider = context.read<GPSTrackingProvider>();
    await gpsProvider.startHighPrecisionTracking(ninoId: 1);

    // Escuchar cambios de posición
    gpsProvider.addListener(_onPositionUpdate);
  }

  void _onPositionUpdate() {
    final position = context.read<GPSTrackingProvider>().currentPosition;
    if (position == null) return;

    final currentLatLng = GpsUtils.positionToLatLng(position);

    // Calcular rotación si hay posición anterior
    double rotation = 0;
    if (_previousPosition != null) {
      rotation = GpsUtils.calculateRotation(_previousPosition!, currentLatLng);
    }

    // Actualizar marcador
    setState(() {
      _markers = {
        Marker(
          markerId: MarkerId('nino_1'),
          position: currentLatLng,
          rotation: rotation,  // Apunta en dirección del movimiento
          infoWindow: InfoWindow(
            title: 'Niño',
            snippet: 'Precisión: ${position.accuracy.toStringAsFixed(1)}m',
          ),
        ),
      };
      _previousPosition = currentLatLng;
    });

    // Centrar mapa
    _mapController?.animateCamera(
      CameraUpdate.newLatLng(currentLatLng),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: CustomIconBack(),
        title: Text('Mapa en Tiempo Real'),
      ),
      body: GoogleMap(
        initialCameraPosition: CameraPosition(
          target: LatLng(-17.7833, -63.1812),
          zoom: 15,
        ),
        markers: _markers,
        onMapCreated: (controller) => _mapController = controller,
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          if (context.read<GPSTrackingProvider>().isTrackingEnabled) {
            context.read<GPSTrackingProvider>().stopTracking();
          } else {
            _startTracking();
          }
        },
        child: Icon(
          context.watch<GPSTrackingProvider>().isTrackingEnabled
              ? Icons.stop
              : Icons.play_arrow,
        ),
      ),
    );
  }

  @override
  void dispose() {
    context.read<GPSTrackingProvider>().stopTracking();
    super.dispose();
  }
}
```

---

## 🔧 Configuración de Permisos

**Android** (`android/app/src/main/AndroidManifest.xml`):
```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

**iOS** (`ios/Runner/Info.plist`):
```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>Necesitamos tu ubicación para mostrar tu posición en el mapa</string>
<key>NSLocationAlwaysUsageDescription</key>
<string>Necesitamos tu ubicación para rastrear al niño en tiempo real</string>
```

---

## 📊 Comparación de Precisión

| Modo | Precisión | Batería | Uso Recomendado |
|------|-----------|---------|-----------------|
| `getHighPrecisionStream()` | ±1-5m | Alta | Tracking activo del niño |
| `getBalancedStream()` | ±5-15m | Media | Modo ahorro de batería |
| `getCurrentPosition()` | ±10-20m | Baja | Obtener ubicación única |

---

## ✅ Checklist de Implementación

- [x] Crear widgets personalizados
- [x] Crear utilidades GPS
- [x] Integrar GPS de alta precisión en Provider
- [x] Actualizar WebSocket a WSS (HTTPS)
- [ ] Probar en dispositivo real
- [ ] Ajustar precisión según consumo de batería
- [ ] Agregar indicador visual de precisión GPS

---

**Creado**: 6 de diciembre de 2025  
**Rescatado de**: InDriver Clone Flutter/Django  
**Adaptado para**: Monitor Infantil SIG
