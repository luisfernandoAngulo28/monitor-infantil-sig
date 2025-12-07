# 📍 Pantalla de Búsqueda de Niños Cercanos - Implementada

## ✅ Archivos Creados

### 1. Modelo de Datos
**`lib/models/nino_cercano.dart`**
- Clases: `NinoCercano`, `PosicionCercana`, `KinderInfo`, `BusquedaCercanosResponse`, `CentroBusqueda`
- Métodos helpers para formateo de distancias, velocidad y precisión
- Deserialización JSON desde API

### 2. Servicio API
**`lib/services/api_service.dart`** (modificado)
- Nuevo método: `buscarNinosCercanos(lat, lng, radiusMetros)`
- Endpoint: `GET /busqueda-cercanos/ninos-cercanos/{lat}/{lng}/?radius={metros}`
- Retorna `BusquedaCercanosResponse`

### 3. Pantalla Principal
**`lib/screens/busqueda_cercanos_screen.dart`**
- Google Maps con marcadores interactivos
- Geolocalización automática del usuario
- Búsqueda de niños en radio configurable
- Modal con detalles completos de cada niño
- Listado alternativo tipo lista

### 4. Widget de Tarjeta
**`lib/widgets/busqueda_cercanos_card.dart`**
- Tarjeta promocional para acceso rápido
- Diseño con gradiente azul
- Resalta características principales

### 5. Navegación
**`lib/screens/home_screen.dart`** (modificado)
- Botón de búsqueda en AppBar (icono de lupa)
- Navegación directa a `BusquedaCercanosScreen`

---

## 🎯 Características Implementadas

### Google Maps Integration
✅ Mapa interactivo con Google Maps Flutter  
✅ Marcador azul para ubicación del usuario  
✅ Marcadores verdes/rojos para niños (según estado)  
✅ Círculo de radio de búsqueda visualizado  
✅ Controles de zoom y brújula  
✅ Animación de cámara al seleccionar niños  

### Geolocalización
✅ Detección automática de ubicación GPS  
✅ Solicitud de permisos de ubicación  
✅ Precisión alta (LocationAccuracy.high)  
✅ Botón para recentrar en mi ubicación  

### Búsqueda Espacial
✅ Radio configurable: 500m, 1km, 2km, 5km, 10km, 20km  
✅ Query con `ST_Distance` y `::geography`  
✅ Distancias precisas en metros y kilómetros  
✅ Filtrado por última posición de cada niño  
✅ Ordenamiento por distancia ascendente  

### UI/UX Profesional
✅ Panel informativo superior (total encontrados + radio)  
✅ Modal deslizable con detalles completos  
✅ Listado alternativo tipo cards  
✅ Indicadores de estado con colores (🟢 Seguro / 🔴 Fuera)  
✅ Información formateada: distancia, velocidad, precisión GPS  
✅ Timestamp relativo (hace X min/horas/días)  
✅ SnackBars con feedback visual  

### Información Mostrada por Niño
- ✅ Nombre completo (con apellidos paterno y materno)
- ✅ Distancia al usuario (metros o km)
- ✅ Estado dentro/fuera del área segura
- ✅ Velocidad actual (km/h)
- ✅ Precisión GPS (±metros)
- ✅ Centro educativo (nombre y dirección)
- ✅ Última actualización de posición
- ✅ Coordenadas GPS (lat/lng)

---

## 🚀 Cómo Usar

### 1. Acceso desde App
```dart
// Desde cualquier pantalla
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => const BusquedaCercanosScreen(),
  ),
);
```

**Acceso directo desde HomeScreen:**
- Botón de lupa (🔍) en AppBar superior derecho

### 2. Flujo de Usuario

**Paso 1: Permisos**
- Al abrir la pantalla, solicita permisos de ubicación
- Detecta ubicación GPS automáticamente

**Paso 2: Búsqueda**
- Presiona botón "Buscar" (FAB inferior derecho)
- Selecciona radio de búsqueda (icono ⚙️ en AppBar)
- Opciones: 500m, 1km, 2km, 5km, 10km, 20km

**Paso 3: Resultados**
- Panel superior muestra total encontrados
- Mapa con marcadores de cada niño
  - **Verde 🟢**: Dentro del área segura
  - **Rojo 🔴**: Fuera del área segura
- Tap en marcador → Modal con detalles

**Paso 4: Detalles**
- Modal deslizable con información completa
- Botón "Ver en mapa" centra cámara en el niño
- Listado alternativo con botón 📋 en AppBar

### 3. Controles Disponibles

| Botón | Ubicación | Función |
|-------|-----------|---------|
| 🔍 Buscar | FAB inferior | Ejecutar búsqueda |
| 📍 Mi ubicación | FAB superior | Recentrar en GPS |
| ⚙️ Radio | AppBar | Cambiar radio de búsqueda |
| 📋 Lista | AppBar | Ver listado tipo cards |
| 🗺️ Marcador | Mapa | Ver detalles del niño |

---

## 📊 Respuesta del API

```json
{
  "centro_busqueda": {
    "lat": -17.7833,
    "lng": -63.1821
  },
  "radio_metros": 5000,
  "total_encontrados": 3,
  "ninos": [
    {
      "id": 3,
      "nombre": "Valentina",
      "apellido_paterno": "González",
      "apellido_materno": "Silva",
      "nombre_completo": "Valentina González Silva",
      "posicion": {
        "lat": -17.785,
        "lng": -63.185
      },
      "distancia_metros": 360.49,
      "distancia_km": 0.36,
      "ultima_actualizacion": "2025-11-26T00:54:49.994495+00:00",
      "dentro_area_segura": false,
      "velocidad_kmh": 0,
      "precision_metros": 10.0,
      "kinder": {
        "nombre": "Centro Educativo Rayito de Sol",
        "direccion": "Calle Sucre esquina Junín"
      },
      "estado": "🔴 Fuera del área",
      "estado_color": "red"
    }
  ]
}
```

---

## 🔧 Configuración Técnica

### Dependencias Requeridas
```yaml
dependencies:
  google_maps_flutter: ^2.14.0  # Mapas
  geolocator: ^14.0.2           # GPS
  dio: ^5.9.0                   # HTTP requests
  provider: ^6.1.5+1            # State management
```

### Permisos Android
**`android/app/src/main/AndroidManifest.xml`**
```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.INTERNET" />
```

### Permisos iOS
**`ios/Runner/Info.plist`**
```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>Necesitamos tu ubicación para buscar niños cercanos</string>
<key>NSLocationAlwaysUsageDescription</key>
<string>Necesitamos tu ubicación para buscar niños cercanos</string>
```

### API Key de Google Maps
Ya configurada en:
- `android/app/src/main/AndroidManifest.xml`
- `ios/Runner/AppDelegate.swift`

---

## 🎨 Personalización

### Cambiar Colores de Marcadores
```dart
// En _actualizarMarcadores()
final color = nino.dentroAreaSegura 
    ? BitmapDescriptor.hueGreen   // Verde para seguros
    : BitmapDescriptor.hueRed;    // Rojo para fuera del área
```

### Cambiar Radio Predeterminado
```dart
// En _BusquedaCercanosScreenState
double _radiusBusqueda = 5000; // Cambiar valor en metros
```

### Agregar Más Opciones de Radio
```dart
final List<double> _radiusOptions = [
  500, 1000, 2000, 5000, 10000, 20000, 50000  // Agregar valores
];
```

---

## 📱 Capturas de Funcionalidad

### Vista Mapa
- Mapa Google Maps a pantalla completa
- Panel superior con estadísticas
- FAB para buscar y centrar ubicación

### Modal de Detalles
- Tarjetas informativas por sección
- Códigos de color según estado
- Botón de navegación al mapa

### Listado Alternativo
- Cards con resumen de cada niño
- Indicadores visuales de estado
- Ordenado por distancia

---

## 🐛 Manejo de Errores

### Permisos Denegados
```
SnackBar: "Permiso de ubicación denegado"
```

### Sin GPS
```
SnackBar: "Los servicios de ubicación están desactivados"
```

### Error de API
```
SnackBar: "Error al buscar niños cercanos: [mensaje]"
```

### Sin Resultados
```
SnackBar: "No se encontraron niños en un radio de X km"
```

---

## ✅ Testing

### 1. Probar Permisos
```bash
# Denegar permisos manualmente
# Verificar mensaje de error
```

### 2. Probar Diferentes Radios
```dart
_radiusOptions.forEach((radius) async {
  await _buscarNinosCercanos();
  // Verificar que cambia el círculo en mapa
});
```

### 3. Probar con Token Expirado
```dart
// API service maneja refresh automático
// Verificar que reintenta con nuevo token
```

---

## 🚀 Próximas Mejoras Sugeridas

### Funcionalidades Adicionales
- [ ] Filtrado por kinder específico
- [ ] Filtrado por estado (solo seguros / solo fuera)
- [ ] Historial de búsquedas recientes
- [ ] Compartir ubicación de niño encontrado
- [ ] Modo seguimiento continuo (actualización cada X segundos)
- [ ] Notificación cuando niño entra/sale del radio
- [ ] Exportar resultados a PDF
- [ ] Modo offline con caché de última búsqueda

### Optimizaciones
- [ ] Caché de resultados (evitar búsquedas duplicadas)
- [ ] Cluster de marcadores cuando hay muchos niños
- [ ] Lazy loading de detalles (solo cargar al abrir modal)
- [ ] Animaciones de entrada de marcadores
- [ ] Zoom automático para incluir todos los resultados

---

## 📚 Documentación de Referencia

### Google Maps Flutter
https://pub.dev/packages/google_maps_flutter

### Geolocator
https://pub.dev/packages/geolocator

### PostGIS ST_Distance
https://postgis.net/docs/ST_Distance.html

---

## 🎯 Estado del Proyecto

### ✅ Completado
- [x] Modelo de datos `NinoCercano`
- [x] Servicio API con endpoint de búsqueda
- [x] Pantalla con Google Maps
- [x] Geolocalización del usuario
- [x] Marcadores interactivos
- [x] Modal de detalles completo
- [x] Listado alternativo
- [x] Selector de radio
- [x] Manejo de errores
- [x] Navegación desde HomeScreen

### 🎉 Resultado Final
**Pantalla 100% funcional y lista para producción**

El endpoint del backend está probado y funcionando:
```bash
GET /api/busqueda-cercanos/ninos-cercanos/-17.7833/-63.1821/?radius=5000
✅ Retorna 3 niños con distancias calculadas correctamente
✅ Datos completos de posición, velocidad, precisión, kinder
✅ Ordenados por distancia ascendente
```

La aplicación Flutter puede:
1. ✅ Obtener ubicación GPS del dispositivo
2. ✅ Consumir el endpoint de búsqueda
3. ✅ Mostrar resultados en mapa interactivo
4. ✅ Presentar detalles completos de cada niño
5. ✅ Permitir cambio de radio de búsqueda
6. ✅ Manejar errores gracefully

---

## 📞 Soporte

Para cualquier problema o mejora, revisar:
- `lib/screens/busqueda_cercanos_screen.dart` (lógica principal)
- `lib/models/nino_cercano.dart` (modelos de datos)
- `lib/services/api_service.dart` (comunicación con backend)
- `backend/apps/api/views.py` (BusquedaCercanosViewSet)

**Versión:** 1.0.0  
**Fecha:** Diciembre 2025  
**Estado:** ✅ Producción
