# 🧱 Stack Tecnológico - Monitor Infantil SIG

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                     APLICACIÓN MÓVIL (TUTOR)                    │
│                    Flutter + Dart (Android/iOS)                 │
│  - flutter_map / google_maps_flutter                            │
│  - http / dio (consumo API)                                     │
│  - firebase_messaging (notificaciones)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │ REST API (JSON)
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      BACKEND API REST                           │
│              Django 5.0 + Django REST Framework                 │
│  - GeoDjango (análisis espacial)                               │
│  - JWT Authentication                                           │
│  - Firebase Admin SDK (push notifications)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                 BASE DE DATOS GEOESPACIAL                       │
│                  PostgreSQL 15 + PostGIS 3.4                    │
│  - Polígonos (áreas de kinders)                                │
│  - Puntos GPS (posiciones de niños)                            │
│  - Consultas espaciales (ST_Within, ST_Contains)               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    HERRAMIENTAS SIG                             │
│                    QGIS / ArcGIS                                │
│  - Digitalización de polígonos                                 │
│  - Validación de capas                                          │
│  - Generación de mapas para informe                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ Aplicación Móvil (Madre/Tutor)

### Tecnologías
- **Framework**: Flutter 3.x
- **Lenguaje**: Dart
- **Plataforma**: Android (prioritario) + iOS (opcional)

### Librerías Principales

```yaml
dependencies:
  # Mapas
  flutter_map: ^6.0.0
  latlong2: ^0.9.0
  # O alternativa Google Maps:
  # google_maps_flutter: ^2.5.0
  
  # HTTP Client
  dio: ^5.4.0
  
  # Geolocalización
  geolocator: ^10.1.0
  location: ^5.0.0
  
  # Notificaciones Push
  firebase_core: ^2.24.0
  firebase_messaging: ^14.7.0
  flutter_local_notifications: ^16.3.0
  
  # Estado
  provider: ^6.1.0
  
  # JWT
  flutter_secure_storage: ^9.0.0
```

### Funcionalidades de la App
1. **Login de tutor** (JWT)
2. **Visualización del mapa** con:
   - Área del kinder (polígono)
   - Última posición del niño
   - Estado: dentro/fuera
3. **Recepción de alertas push**
4. **Historial de posiciones**
5. **Panel de control** (batería, última actualización)

---

## 2️⃣ Backend / API - **✅ YA IMPLEMENTADO**

### Tecnologías
- **Framework**: Django 5.0
- **Extensiones**:
  - ✅ GeoDjango → análisis espacial
  - ✅ Django REST Framework → API REST
  - ✅ djangorestframework-gis → GeoJSON
  - ✅ djangorestframework-simplejwt → autenticación

### Endpoints API Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/token/` | Obtener JWT token |
| POST | `/api/token/refresh/` | Refrescar token |
| GET | `/api/ninos/` | Listar niños del tutor |
| GET | `/api/ninos/{id}/estado/` | Estado actual (dentro/fuera) |
| POST | `/api/ninos/{id}/registrar_posicion/` | **Enviar GPS del niño** |
| GET | `/api/ninos/{id}/historial/` | Historial de posiciones |
| GET | `/api/mis-alertas/` | Alertas del tutor |
| POST | `/api/alertas/{id}/marcar_leida/` | Marcar alerta como leída |
| GET | `/api/centros/` | Centros educativos (polígonos) |
| POST | `/api/configuracion/actualizar_firebase_token/` | Token FCM |

### Análisis Espacial GeoDjango

```python
# En PosicionGPS.save() - AUTOMÁTICO
area_kinder = self.nino.centro_educativo.area_segura
self.dentro_area_segura = area_kinder.contains(self.ubicacion)

# Si está fuera, genera alerta automáticamente
if not self.dentro_area_segura:
    Alerta.crear_alerta_salida(self)
```

---

## 3️⃣ Base de Datos Geoespacial - **✅ CONFIGURADA**

### Tecnologías
- **Motor**: PostgreSQL 15
- **Extensión**: PostGIS 3.4
- **ORM**: Django ORM + GeoDjango

### Modelos Principales

```python
# Centro Educativo (Kinder)
class CentroEducativo(models.Model):
    area_segura = gis_models.PolygonField(srid=4326)  # Polígono
    ubicacion_centro = gis_models.PointField(srid=4326)  # Centroide

# Posición GPS del Niño
class PosicionGPS(models.Model):
    ubicacion = gis_models.PointField(srid=4326)  # Punto GPS
    dentro_area_segura = models.BooleanField()  # Calculado automáticamente
```

### Consultas Espaciales Disponibles

```python
# ST_Within (PostGIS) → GeoDjango: contains()
area_kinder.contains(punto_nino)

# ST_Distance
punto_nino.distance(centro_kinder)

# ST_Buffer (margen de tolerancia)
area_con_margen = area_kinder.buffer(metros)
```

---

## 4️⃣ Herramientas SIG de Escritorio

### QGIS (Recomendado - Software Libre)

**Uso en el proyecto:**
1. **Digitalización del polígono del Kinder**:
   - Crear nueva capa vectorial (Polygon, EPSG:4326)
   - Digitalizar manualmente el área del kinder
   - Exportar a Shapefile o GeoJSON

2. **Importar a Django**:
   ```python
   from django.contrib.gis.utils import LayerMapping
   # Cargar shapefile a PostgreSQL/PostGIS
   ```

3. **Generar mapas para el informe**:
   - Print Composer / Layout
   - Exportar a PDF/PNG para documentación

### Alternativa: Django Admin GIS

Ya implementado en el proyecto:
- Panel admin con mapa interactivo
- Dibujar polígonos directamente en el navegador
- Editar geometrías visualmente

---

## 5️⃣ Notificaciones y Alertas - **✅ IMPLEMENTADO**

### Mínimo (Estado en la App)
```dart
// Flutter - Mostrar alerta roja
if (!estado.dentroAreaSegura) {
  showDialog(
    context: context,
    builder: (_) => AlertDialog(
      backgroundColor: Colors.red,
      title: Text('⚠️ ALERTA'),
      content: Text('${nino.nombre} ha salido del área segura!'),
    ),
  );
}
```

### Opcional Pro: Firebase Cloud Messaging - **✅ YA CONFIGURADO**

**Backend (Django):**
```python
# apps/alerts/services.py - YA IMPLEMENTADO
NotificacionService.enviar_push_notification(tutor, alerta)
```

**Flutter:**
```dart
// Recibir notificaciones
FirebaseMessaging.onMessage.listen((message) {
  // Mostrar alerta local
  LocalNotification.show(message);
});
```

---

## 6️⃣ Infraestructura y Desarrollo

### Control de Versiones
- ✅ Git (`.gitignore` creado)
- GitHub/GitLab para repositorio

### Entorno Backend

**Desarrollo Local:**
```bash
# Opción 1: Sin Docker
python -m venv venv
venv\Scripts\activate
pip install -r requirements/dev.txt
python manage.py runserver

# Opción 2: Con Docker - ✅ YA CONFIGURADO
docker-compose up -d
```

**Despliegue Opcional:**
- **Railway**: Deploy automático desde GitHub
- **Render**: Free tier con PostgreSQL
- **PythonAnywhere**: Hosting Django gratis
- **VPS** (DigitalOcean, Linode)

### Entorno Móvil

```bash
# Instalar Flutter SDK
flutter doctor

# Crear proyecto
flutter create monitor_infantil_app
cd monitor_infantil_app

# Ejecutar en Android
flutter run
```

---

## 📱 Próximo Paso: Crear App Flutter

### Estructura Sugerida

```
monitor_infantil_app/
├── lib/
│   ├── main.dart
│   ├── models/
│   │   ├── nino.dart
│   │   ├── posicion_gps.dart
│   │   └── alerta.dart
│   ├── services/
│   │   ├── api_service.dart       # Consumir Django API
│   │   ├── auth_service.dart      # Login JWT
│   │   └── notification_service.dart  # FCM
│   ├── screens/
│   │   ├── login_screen.dart
│   │   ├── mapa_screen.dart       # Mapa principal
│   │   ├── alertas_screen.dart
│   │   └── historial_screen.dart
│   └── widgets/
│       ├── mapa_widget.dart
│       └── estado_nino_card.dart
```

---

## 🎯 Resumen de Compatibilidad

| Componente | Tu Propuesta | Estado Actual |
|------------|-------------|---------------|
| App Móvil | Flutter + Dart | ⏳ Por crear |
| Backend | Django + GeoDjango | ✅ Completo |
| API REST | DRF | ✅ Completo |
| Base de Datos | PostgreSQL + PostGIS | ✅ Configurado |
| Análisis Espacial | GeoDjango | ✅ Implementado |
| SIG Escritorio | QGIS/ArcGIS | 📝 Documentado |
| Notificaciones | FCM | ✅ Backend listo |
| Docker | Opcional | ✅ docker-compose.yml |

---

## 🚀 Comandos para Empezar

### 1. Levantar Backend (que ya tienes)
```bash
cd c:\ProyectoSig
docker-compose up -d db
python manage.py migrate
python manage.py runserver
```

### 2. Crear App Flutter
```bash
flutter create monitor_infantil_app
cd monitor_infantil_app
flutter pub add dio flutter_map firebase_messaging geolocator provider
flutter run
```

¿Quieres que creemos ahora la app móvil Flutter? 📱
