# 📍 Sistema SIG de Monitoreo Infantil

**Proyecto Académico**: INF442-SA (2025) - Ing. Franklin Calderón Flores

## 📋 Descripción

Sistema de información geográfica para monitoreo en tiempo real de niños preescolares en centros educativos (Kinders), detectando automáticamente cuando salen del área segura mediante análisis espacial point-in-polygon.

## 🏗️ Estructura del Proyecto

```
SIG22/
├── backend/              # 🔧 API Django + GeoDjango
│   ├── apps/            # Módulos: core, gis_tracking, alerts, api
│   ├── config/          # Configuración Django
│   ├── templates/       # Templates web
│   ├── requirements/    # Dependencias Python
│   └── manage.py
│
├── web/                 # 🌐 Frontend Web (Django Templates + Leaflet)
│   └── static/          # CSS, JS, imágenes (futuro)
│
├── mobile/              # 📱 App Móvil Flutter
│   └── monitor_infantil_app/  # Proyecto Flutter
│
└── SIG22/               # 📚 Documentación del Proyecto
    ├── docs/            # Tutoriales y guías
    └── scripts/         # Scripts útiles
```

## 🧱 Stack Tecnológico

### Backend
- **Framework**: Django 5.0 + GeoDjango
- **Base de Datos**: PostgreSQL 15 + PostGIS 3.4
- **API**: Django REST Framework + djangorestframework-gis
- **Auth**: JWT (Simple JWT)
- **Tasks**: Celery + Redis

### Frontend Web
- **Templates**: Django Templates
- **Mapas**: Leaflet.js + OpenStreetMap
- **UI**: Bootstrap 5

### Mobile
- **Framework**: Flutter 3.x + Dart
- **Mapas**: flutter_map
- **HTTP**: Dio
- **Notificaciones**: Firebase Cloud Messaging

### Herramientas SIG
- **QGIS**: Digitalización de polígonos
- **PostGIS**: Consultas espaciales (ST_Within, ST_Contains)

## 🚀 Inicio Rápido

### 1. Backend (Obligatorio)

```bash
cd backend

# Instalar dependencias
python -m venv venv
venv\Scripts\activate
pip install -r requirements/dev.txt

# Levantar base de datos
docker-compose up -d db

# Migrar
python manage.py migrate
python manage.py createsuperuser

# Ejecutar
python manage.py runserver
```

**URLs:**
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Dashboard: http://localhost:8000/

### 2. Mobile (Opcional)

```bash
cd mobile

# Crear proyecto Flutter
flutter create monitor_infantil_app
cd monitor_infantil_app

# Instalar dependencias
flutter pub add dio flutter_map provider firebase_messaging

# Ejecutar
flutter run
```

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [README.md](README.md) | Este archivo |
| [STACK_TECNOLOGICO.md](STACK_TECNOLOGICO.md) | Arquitectura y stack completo |
| [INSTALACION.md](INSTALACION.md) | Guía de instalación detallada |
| [docs/TUTORIAL.md](docs/TUTORIAL.md) | Tutorial paso a paso |
| [docs/FLUTTER_APP.md](docs/FLUTTER_APP.md) | Guía Flutter con código |
| [docs/QGIS_TUTORIAL.md](docs/QGIS_TUTORIAL.md) | Digitalización con QGIS |
| [RESUMEN_PROYECTO.md](RESUMEN_PROYECTO.md) | Resumen ejecutivo |

## 🎯 Características

### Backend
- ✅ Análisis espacial point-in-polygon (GeoDjango)
- ✅ 15+ endpoints REST con GeoJSON
- ✅ Sistema de alertas automático con cooldown
- ✅ Notificaciones push (Firebase)
- ✅ Panel admin con editor de mapas GIS
- ✅ Tests unitarios

### Web
- ✅ Dashboard con estadísticas
- ✅ Mapa interactivo Leaflet
- ✅ Visualización de alertas en tiempo real
- ✅ Auto-refresh cada 30 segundos

### Mobile (En desarrollo)
- ⏳ Login JWT
- ⏳ Mapa con flutter_map
- ⏳ Notificaciones push
- ⏳ Gestión de alertas

## 🔧 Desarrollo

### Backend
```bash
cd backend
python manage.py runserver
python manage.py test
```

### Mobile
```bash
cd mobile/monitor_infantil_app
flutter run
flutter test
```

## 📡 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/token/` | Login (JWT) |
| GET | `/api/ninos/` | Listar niños |
| POST | `/api/ninos/{id}/registrar_posicion/` | Enviar GPS |
| GET | `/api/ninos/{id}/estado/` | Estado (dentro/fuera) |
| GET | `/api/mis-alertas/` | Alertas del tutor |

Ver: `backend/apps/api/API_DOCS.md`

## 🗄️ Base de Datos

### Modelos Principales

```python
# Centro Educativo (Kinder)
class CentroEducativo(models.Model):
    area_segura = gis_models.PolygonField(srid=4326)  # Polígono

# Posición GPS del Niño
class PosicionGPS(models.Model):
    ubicacion = gis_models.PointField(srid=4326)  # Punto
    dentro_area_segura = models.BooleanField()  # Calculado automáticamente
```

### Análisis Espacial
```python
# Detección automática en PosicionGPS.save()
area_kinder.contains(ubicacion_nino)  # ST_Within en PostGIS
```

## 🎓 Objetivos Académicos

### Cumplimiento de Requisitos

✅ **Base de datos geoespacial**: PostgreSQL + PostGIS  
✅ **Análisis espacial**: Point-in-polygon con GeoDjango  
✅ **Aplicación SIG**: Django + API REST  
✅ **Visualización**: Mapas web (Leaflet) + móvil (Flutter)  
✅ **Alertas**: Sistema automático con notificaciones  
✅ **Herramientas SIG**: QGIS para digitalización  

## 🤝 Contribuir

Este es un proyecto académico. Para reportar issues o sugerencias:
1. Revisar la documentación en `SIG22/docs/`
2. Verificar que el backend esté ejecutándose
3. Consultar los README de cada componente

## 📄 Licencia

Proyecto Académico - INF442-SA (2025)  
Universidad [Tu Universidad]

## 👥 Autor

Desarrollado como proyecto académico para la materia INF442-SA  
Docente: Ing. Franklin Calderón Flores

---

## 📞 Soporte

Para soporte técnico:
- Ver documentación en `SIG22/docs/`
- Revisar README de cada componente:
  - `backend/README.md`
  - `web/README.md`
  - `mobile/README.md`

---

**¡Gracias por revisar este proyecto! 🚀**
