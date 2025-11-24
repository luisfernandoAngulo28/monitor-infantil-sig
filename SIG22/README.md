# 📍 Sistema SIG de Monitoreo Infantil

## 📱 Descripción
Sistema de información geográfica para monitoreo en tiempo real de niños preescolares, detectando automáticamente cuando salen del área segura del kinder mediante análisis espacial (GeoDjango).

**Proyecto Académico**: INF442-SA (2025) - Ing. Franklin Calderón Flores

## 🎯 Características Principales
- ✅ **Análisis Espacial Point-in-Polygon**: Detección automática dentro/fuera del área
- ✅ **Tracking GPS en Tiempo Real**: Monitoreo continuo desde celular/smartwatch
- ✅ **Alertas Automáticas**: Notificaciones push cuando niño sale del área
- ✅ **Panel Web Administrativo**: Dashboard con mapa interactivo (Leaflet)
- ✅ **API REST**: Endpoints GeoJSON para app móvil Flutter
- ✅ **Base de Datos Geoespacial**: PostgreSQL + PostGIS

## 🧱 Stack Tecnológico

### 📱 **App Móvil (Tutor/Madre)**
- **Framework**: Flutter + Dart
- **Mapas**: flutter_map / google_maps_flutter
- **HTTP**: Dio
- **Notificaciones**: Firebase Cloud Messaging
- **Plataforma**: Android + iOS

### 🔧 **Backend / API**
- **Framework**: Django 5.0 + GeoDjango
- **API**: Django REST Framework + DRF-GIS
- **Auth**: JWT (djangorestframework-simplejwt)
- **Tasks**: Celery + Redis

### 🗄️ **Base de Datos Geoespacial**
- **Motor**: PostgreSQL 15
- **Extensión**: PostGIS 3.4
- **Geometrías**: Polígonos (áreas) + Puntos (GPS)
- **Consultas**: ST_Within, ST_Contains, ST_Distance

### 🗺️ **Herramientas SIG**
- **QGIS**: Digitalización de polígonos del kinder
- **Django Admin GIS**: Editor de mapas en el navegador
- **Leaflet.js**: Visualización web interactiva

### 🔔 **Notificaciones**
- **Backend**: Firebase Admin SDK (Python)
- **Móvil**: Firebase Cloud Messaging (Flutter)
- **Alertas**: Automáticas con cooldown anti-spam

### Estructura del Proyecto
```
monitor_infantil/
├── config/                 # Configuración Django
├── apps/
│   ├── core/              # Usuarios, autenticación
│   ├── gis_tracking/      # Modelos geoespaciales, tracking GPS
│   ├── alerts/            # Sistema de alertas
│   └── api/               # API REST
├── static/                # CSS, JS, imágenes
├── templates/             # Templates Django
├── requirements/          # Dependencias Python
└── docker/                # Dockerfiles
```

## 🗺️ Modelos de Datos Principales

### CentroEducativo (Polígono)
- nombre, dirección
- area_segura (PolygonField) - Polígono del kinder

### Niño
- nombre, edad, foto
- centro_educativo (FK)
- tutor (FK)
- dispositivo_id

### PosicionGPS (Punto)
- niño (FK)
- ubicacion (PointField) - Punto GPS
- timestamp
- dentro_area_segura (Boolean)

### Alerta
- niño, tutor, tipo_alerta
- posicion_gps (FK)
- enviada, leida

## 🚀 Estado del Proyecto

### ✅ **Fase 1: Backend Completo**
- [x] Django + GeoDjango configurado
- [x] PostgreSQL + PostGIS
- [x] Modelos geoespaciales (CentroEducativo, Niño, PosicionGPS, Alerta)
- [x] Migraciones creadas

### ✅ **Fase 2: Análisis Espacial**
- [x] TrackingService implementado
- [x] Algoritmo point-in-polygon automático
- [x] Detección de salida del área con alertas

### ✅ **Fase 3: API REST**
- [x] 15+ endpoints implementados
- [x] Autenticación JWT
- [x] Serializers GeoJSON
- [x] Sistema de alertas con Firebase

### ✅ **Fase 4: Panel Web**
- [x] Dashboard con estadísticas
- [x] Mapa interactivo Leaflet
- [x] Django Admin con editor de polígonos
- [x] Tests unitarios

### ⏳ **Fase 5: App Móvil Flutter** (Siguiente)
- [ ] Pantalla de login
- [ ] Visualización de mapa
- [ ] Consumo de API
- [ ] Notificaciones push

## 📦 Instalación Rápida

```bash
# Clonar proyecto
cd ProyectoSig

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements/dev.txt

# Configurar PostgreSQL + PostGIS
# Ver docker-compose.yml

# Migrar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## 🔧 Requisitos Previos
- Python 3.11+
- PostgreSQL 15 + PostGIS 3.4
- Docker (opcional pero recomendado)
- Gi� Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| [README.md](README.md) | Este archivo - Descripción general |
| [INSTALACION.md](INSTALACION.md) | Guía de instalación paso a paso |
| [STACK_TECNOLOGICO.md](STACK_TECNOLOGICO.md) | Stack completo y arquitectura |
| [docs/TUTORIAL.md](docs/TUTORIAL.md) | Tutorial de uso con ejemplos |
| [docs/FLUTTER_APP.md](docs/FLUTTER_APP.md) | Guía para crear app móvil |
| [docs/QGIS_TUTORIAL.md](docs/QGIS_TUTORIAL.md) | Digitalización con QGIS |
| [apps/api/API_DOCS.md](apps/api/API_DOCS.md) | Documentación API REST |
| [RESUMEN_PROYECTO.md](RESUMEN_PROYECTO.md) | Resumen ejecutivo |

## 🎓 Proyecto Académico
- **Materia**: INF442-SA (2025)
- **Docente**: Ing. Franklin Calderón Flores
- **Institución**: Universidad [Tu Universidad]
- **Tecnología**: GeoDjango + Flutter + PostGIS
## 👥 Equipo
- Desarrollador Backend/SIG
- Desarrollador Frontend
- Especialista en telecomunicaciones

## 📄 Licencia
Proyecto académico - INF442-SA (2025)
