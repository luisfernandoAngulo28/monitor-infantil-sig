# Monitor Infantil SIG - Resumen del Proyecto

**Materia**: INF442-SA (2025)  
**Docente**: Ing. Franklin Calderón Flores  
**Ubicación**: Santa Cruz de la Sierra, Bolivia

---

## ¿Qué estamos haciendo en el proyecto?

Estamos desarrollando un **Sistema de Información Geográfica (SIG) para el Monitoreo de Niños Preescolares en Tiempo Real** llamado "Monitor Infantil SIG". El proyecto consiste en una aplicación móvil que permite a madres o tutores monitorear la ubicación GPS de niños preescolares y recibir alertas automáticas cuando el niño sale de áreas seguras predefinidas (como su centro educativo - Kinder) mediante análisis espacial de información vectorial (Shapefiles/Polígonos).

### Problema que Resuelve:
La falta de sistemas de monitoreo en tiempo real dificulta la toma de decisiones tempranas ante incidentes como:
- **Pérdida del niño** dentro o fuera del centro educativo
- **Accidentes** al salir de áreas seguras
- **Secuestros** en casos extremos

Los controles manuales son laboriosos, costosos y lentos, provocando respuestas tardías. Los SIG ofrecen herramientas óptimas para operaciones espaciales que otros sistemas estándar no pueden realizar.

### Funcionalidades Principales:
- **Tracking GPS en Tiempo Real**: Monitoreo continuo de la posición del niño prescolar
- **Análisis Espacial Automático**: Detección mediante operaciones espaciales (Point-in-Polygon) si el niño está dentro o fuera del área segura
- **Alertas Instantáneas**: Notificaciones push al celular de la madre/tutor cuando el niño sale del área de monitoreo
- **Gestión de Áreas Seguras (Polígonos)**: Definición de zonas geográficas de seguridad (Kinder, casa, parque) como geometrías vectoriales
- **Base de Datos Geoespacial**: Almacenamiento de datos espaciales (puntos, polígonos) y alfanuméricos
- **Historial de Ubicaciones**: Registro de trayectorias y movimientos
- **WebSocket para Comunicación Instantánea**: Actualizaciones en tiempo real sin demora
- **Monitoreo de Batería**: Control del nivel de batería del dispositivo del niño
- **Sistema de Autenticación**: Login seguro para madres/tutores con gestión de permisos

---

## Objetivos del Proyecto (SMART)

### **Objetivo General:**
Diseñar e implementar un sistema de información geográfica que permita el monitoreo en tiempo real de la posición de niños preescolares y emitir alertas automáticas en caso de que salgan de áreas seguras definidas.

### **Objetivos Específicos:**
1. **Crear una base de datos geoespacial** que almacene:
   - Datos de áreas o unidades educativas (polígonos vectoriales)
   - Posiciones GPS de niños (puntos geográficos)
   - Datos alfanuméricos de tutores, niños y eventos

2. **Desarrollar una aplicación móvil** que permita:
   - Visualización de información geográfica en mapas interactivos
   - Generación automática de alertas mediante análisis espacial
   - Monitoreo en tiempo real de ubicaciones

3. **Implementar análisis espacial** utilizando:
   - Operaciones geométricas (Point-in-Polygon, ST_Contains)
   - Detección automática de anomalías en la posición geográfica
   - Generación de alertas basadas en criterios espaciales

4. **Capacitar al personal encargado** (madres, tutores, administradores) en:
   - Uso de la aplicación móvil
   - Interpretación de alertas
   - Mantenimiento básico de la aplicación

---

## ¿Con qué tecnologías lo estamos haciendo?

### **Backend (Servidor) - Componente SIG**
- **Django 5.0+**: Framework web de Python para la API REST
- **Django REST Framework**: Para crear endpoints RESTful geoespaciales
- **GeoDjango**: Extensión de Django para operaciones SIG
- **Django Channels**: Soporte de WebSocket para comunicación en tiempo real
- **Daphne**: Servidor ASGI para manejar HTTP y WebSocket
- **PostgreSQL 16 + PostGIS**: Base de datos espacial con capacidades GIS completas
  - **PostGIS**: Extensión geoespacial que permite operaciones como:
    - `ST_Contains()`: Verificar si un punto está dentro de un polígono
    - `ST_Distance()`: Calcular distancias entre geometrías
    - `ST_Area()`: Calcular área de polígonos
    - Almacenamiento de geometrías (Point, Polygon, LineString)
- **Redis**: Sistema de mensajería para canales WebSocket
- **Docker**: Para contenedores (Redis)

### **Frontend (Aplicación Móvil)**
- **Flutter**: Framework multiplataforma para Android/iOS (cumple requisito de app móvil)
- **Dart**: Lenguaje de programación
- **Google Maps Flutter**: Integración de mapas interactivos para visualización SIG
- **Provider**: Gestión de estado reactivo
- **web_socket_channel**: Cliente WebSocket para comunicación en tiempo real
- **Geolocator**: Obtención de coordenadas GPS del dispositivo
- **Permission Handler**: Gestión de permisos de ubicación y notificaciones
- **Flutter Local Notifications**: Sistema de alertas push

### **Infraestructura y Despliegue**
- **DigitalOcean**: Hosting del servidor en la nube (Ubuntu 24.04)
- **Nginx**: Servidor web y proxy inverso
- **Git/GitHub**: Control de versiones
- **SSH**: Acceso remoto al servidor

### **Herramientas SIG y Desarrollo**
- **QGIS**: Para visualización y preparación de datos geoespaciales (shapefiles)
- **GDAL/OGR**: Librería para conversión de formatos geoespaciales
- **VS Code**: Editor de código
- **Python 3.12**: Versión de Python con librerías geoespaciales
- **pip/venv**: Gestión de paquetes y entornos virtuales
- **Flutter SDK**: Kit de desarrollo de Flutter

---

## Metodología de Desarrollo (Alineada con el Enunciado)

### **Fase 1: Recopilación y Preparación de Datos**
**Objetivo**: Obtener datos geoespaciales de áreas de monitoreo

**Actividades Realizadas**:
- ✅ Definición del modelo de datos geoespacial (Point, Polygon)
- ✅ Creación de estructura para almacenar shapefiles de centros educativos
- 🔄 Digitalización de áreas de Kinders en Santa Cruz (en progreso)
- 🔄 Levantamiento de datos en campo con GPS (pendiente)
- ✅ Integración con Google Maps para visualización

**Resultados**:
- Modelo de datos preparado para importar shapefiles
- Sistema de coordenadas definido (WGS84 - EPSG:4326)

### **Fase 2: Diseño de la Base de Datos Geoespacial**
**Objetivo**: Crear modelo de datos que integre capas geográficas y datos alfanuméricos

**Actividades Realizadas**:
- ✅ Diseño del esquema de base de datos con PostgreSQL + PostGIS
- ✅ Creación de tablas con campos geoespaciales:
  - **Tabla Niño**: Datos alfanuméricos (nombre, edad, tutor)
  - **Tabla PosicionGPS**: Geometría Point + timestamp + metadatos
  - **Tabla AreaSegura**: Geometría Polygon + nombre + tipo
  - **Tabla Tutor**: Datos de madres/tutores + credenciales
- ✅ Implementación de índices espaciales para consultas rápidas
- ✅ Configuración de relaciones entre capas espaciales y datos alfanuméricos

**Modelo de Datos**:
```
Tutor (1) ---< (N) Niño (1) ---< (N) PosicionGPS
                 |
                 └---< (N) AreaSegura (Polygon)
```

### **Fase 3: Desarrollo del Sistema**
**Objetivo**: Implementar aplicación con capacidades SIG

**Actividades Realizadas**:
- ✅ Configuración de GeoDjango para operaciones SIG
- ✅ Desarrollo de API REST con endpoints geoespaciales:
  - `/api/areas-seguras/` - CRUD de polígonos de áreas
  - `/api/ninos/` - Gestión de niños
  - `/api/posiciones/` - Histórico de ubicaciones GPS
  - `/api/alertas/` - Registro de alertas generadas
- ✅ Implementación de WebSocket Consumer para tracking en tiempo real
- ✅ Desarrollo de aplicación móvil Flutter con:
  - Mapa interactivo con Google Maps
  - Visualización de polígonos de áreas seguras
  - Marcadores de posición en tiempo real
  - Sistema de alertas push
- ✅ Integración de autenticación JWT para seguridad
- ✅ Despliegue en servidor DigitalOcean con Daphne

### **Fase 4: Análisis Espacial**
**Objetivo**: Realizar análisis espacial para detectar anomalías y emitir alertas

**Análisis Espacial Implementado**:

1. **Operación Point-in-Polygon** (Función principal):
```python
# Verificar si posición GPS del niño está dentro de área segura
dentro_area = area_segura.poligono.contains(posicion_gps.punto)
```

2. **Consulta SQL Espacial con PostGIS**:
```sql
SELECT ST_Contains(
    area_segura.poligono,
    ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)
) AS dentro_area;
```

3. **Lógica de Alerta**:
- Si `ST_Contains() = False` → Niño fuera del área → Generar alerta
- Si `ST_Contains() = True` → Niño dentro del área → Estado normal

4. **Análisis Adicionales**:
- ✅ Cálculo de distancia mínima a área segura (cuando está fuera)
- ✅ Detección de velocidad anormal de movimiento
- ✅ Análisis de batería baja combinado con posición

**Flujo de Análisis Espacial en Tiempo Real**:
```
1. GPS del niño envía coordenadas (lat, lon)
2. Servidor recibe punto geográfico vía WebSocket
3. PostGIS ejecuta ST_Contains(polygon, point)
4. Si resultado = FALSE:
   a. Generar alerta en BD
   b. Enviar notificación push al tutor
   c. Actualizar mapa con marcador ROJO
5. Si resultado = TRUE:
   a. Actualizar posición normal
   b. Mostrar marcador VERDE en mapa
```

---

## ¿Cómo lo estamos haciendo?

### **Arquitectura del Sistema SIG**

El proyecto sigue una **arquitectura Cliente-Servidor con capacidades SIG y comunicación en tiempo real**:

```
[App Flutter Móvil]          [Servidor Django + GeoDjango]        [PostgreSQL + PostGIS]
  - Mapa Google Maps    <-->    - API REST                   <-->    - Geometrías (Point/Polygon)
  - WebSocket Client           - WebSocket Consumer                - Datos alfanuméricos
  - GPS Tracker                - Análisis Espacial                 - Índices espaciales
  - Sistema Alertas            - Motor de Alertas                  
                                      ↓
                                  [Redis]
                               Cache & WebSocket
```

### **Proceso de Desarrollo Detallado**

#### **1. Configuración del Backend**
- Instalación de Django, Django Channels, y dependencias
- Configuración de PostgreSQL con extensión PostGIS
- Creación de modelos de datos (Tutor, Niño, Ubicación, ÁreaSegura)
- Desarrollo de API REST endpoints
- Implementación de WebSocket Consumers para tracking GPS
- Configuración de ASGI para soporte HTTP + WebSocket
- Despliegue en DigitalOcean con Daphne

#### **2. Desarrollo del Frontend**
- Creación de la estructura del proyecto Flutter
- Implementación de Providers para gestión de estado:
  - `AuthProvider`: Autenticación y sesión de usuario
  - `GPSTrackingProvider`: Conexión WebSocket y tracking GPS
- Desarrollo de pantallas:
  - Login/Registro
  - Mapa en tiempo real con marcadores
  - Gestión de niños y áreas seguras
  - Historial de ubicaciones
- Integración con Google Maps API
- Implementación de cliente WebSocket

#### **3. Comunicación en Tiempo Real**
**Flujo WebSocket:**
1. El tutor inicia sesión en la app
2. La app establece conexión WebSocket: `ws://servidor/ws/tracking/tutor/{id}/`
3. El servidor autentica la conexión
4. Cuando un niño envía su ubicación GPS:
   - El servidor valida si está en área segura
   - Calcula nivel de batería
   - Envía actualización al tutor vía WebSocket
5. La app actualiza el mapa en tiempo real sin recargar

**Formato de mensajes WebSocket:**
```json
{
  "type": "gps_update",
  "nino_id": 1,
  "ubicacion": {"latitude": -17.7833, "longitude": -63.1812},
  "dentro_area_segura": true,
  "nivel_bateria": 85,
  "timestamp": "2025-11-28T10:30:00Z"
}
```

#### **4. Gestión de Datos Geoespaciales**
- Uso de **PostGIS** para cálculos geográficos
- Función `ST_Contains()` para verificar si un punto está dentro de un polígono (área segura)
- Almacenamiento de coordenadas en formato `PointField` y `PolygonField`
- Consultas espaciales optimizadas

#### **5. Despliegue en Producción**
**Pasos realizados:**
1. Configuración del droplet en DigitalOcean (Ubuntu 24.04)
2. Instalación de dependencias del sistema
3. Clonación del repositorio Git
4. Configuración de variables de entorno (`.env`)
5. Instalación de Redis con Docker
6. Configuración de PostgreSQL gestionado
7. Ejecución de migraciones de base de datos
8. Inicio del servidor Daphne para ASGI
9. (Pendiente) Configuración de Nginx como proxy inverso
10. (Pendiente) Configuración de SSL/HTTPS con Let's Encrypt

#### **6. Metodología de Trabajo**
- **Desarrollo iterativo**: Implementación por fases (autenticación → API → WebSocket → frontend)
- **Testing continuo**: Pruebas con script `test_websocket.py` para validar conexiones
- **Versionamiento**: Git para control de versiones y respaldo de código
- **Documentación en código**: Comentarios y docstrings en Python/Dart

### **Desafíos Resueltos**
1. ✅ Configuración de GeoDjango con PostGIS para análisis espacial
2. ✅ Implementación de operaciones Point-in-Polygon en tiempo real
3. ✅ Configuración de Django Channels para WebSocket
4. ✅ Integración de Google Maps en Flutter con geometrías personalizadas
5. ✅ Gestión de estado reactivo en Flutter con Provider
6. ✅ Instalación y configuración de Redis para mensajería
7. ✅ Despliegue de Daphne en DigitalOcean
8. 🔄 Configuración de archivos WebSocket en el servidor (en progreso)
9. 🔄 Optimización de consultas espaciales con índices GiST

### **Próximos Pasos**
1. Subir archivos `consumers.py` y `routing.py` al servidor
2. Actualizar `asgi.py` con configuración de WebSocket
3. Reiniciar Daphne y probar conexión WebSocket
4. Importar shapefiles de Kinders de Santa Cruz a la base de datos
5. Configurar Nginx para proxy inverso
6. Implementar SSL/HTTPS con Let's Encrypt
7. Configurar Supervisor para auto-reinicio del servidor
8. Realizar pruebas completas de análisis espacial
9. Capacitación a madres/tutores en uso de la aplicación
10. Documentación técnica y manual de usuario

---

## Alcance del Proyecto

### **Incluye:**
- ✅ Diseño de base de datos espacial (PostgreSQL + PostGIS) y alfanumérica
- ✅ Desarrollo de aplicación móvil Flutter para Android/iOS
- ✅ Implementación de análisis espacial en tiempo real (Point-in-Polygon)
- ✅ Sistema de alertas automáticas mediante WebSocket
- ✅ API REST para operaciones CRUD geoespaciales
- ✅ Servidor de producción en DigitalOcean
- ✅ Sistema de autenticación y permisos
- 🔄 Importación de shapefiles de áreas educativas
- 🔄 Manual de usuario y documentación técnica
- 🔄 Capacitación inicial a usuarios (madres/tutores)
- ⏳ Propuesta de soporte técnico inicial (3 meses)

### **Hardware Propuesto (Requisitos):**
- **Servidor**: 
  - Droplet DigitalOcean (2 vCPU, 4GB RAM, 80GB SSD) - ✅ Implementado
  - PostgreSQL 16 gestionado con PostGIS - ✅ Implementado
  
- **Dispositivos de Usuario**:
  - Smartphones Android 8.0+ o iOS 12+ para madres/tutores
  - Dispositivo GPS con conectividad para niños (smartwatch o teléfono básico)

- **Equipos de Red y Comunicación**:
  - Conexión a internet móvil (3G/4G/5G) para GPS en tiempo real
  - Red WiFi en centros educativos (opcional para backup)

### **Software Implementado:**
- **SIG**: GeoDjango + PostGIS (capacidades equivalentes a ArcGIS)
- **Sistema de Gestión de BD**: PostgreSQL 16 con extensión PostGIS
- **Servidor**: Daphne (ASGI) + Nginx
- **Aplicación**: Flutter (multiplataforma)

### **Personal del Proyecto:**
- ✅ Desarrollador Full Stack (Backend Django + Frontend Flutter)
- ✅ Especialista en SIG (GeoDjango + PostGIS)
- 🔄 Cartógrafo (digitalización de áreas educativas - en progreso)
- ⏳ Experto en redes (configuración SSL/Nginx - pendiente)
- ⏳ Capacitador (entrenamiento a usuarios finales - pendiente)

---

## Recursos del Proyecto

### **Recursos Tecnológicos**

| Categoría | Recurso | Estado | Observación |
|-----------|---------|--------|-------------|
| **Servidor** | DigitalOcean Droplet 2vCPU/4GB RAM | ✅ Activo | IP: 143.198.30.170 |
| **Base de Datos** | PostgreSQL 16 + PostGIS | ✅ Operativa | BD gestionada en DigitalOcean |
| **Cache** | Redis (Docker) | ✅ Corriendo | Puerto 6379 |
| **Servidor App** | Daphne ASGI | ✅ Corriendo | Puerto 8000 |
| **Proxy** | Nginx | ⏳ Pendiente | Configuración en progreso |
| **SSL** | Let's Encrypt | ⏳ Pendiente | Post-Nginx |
| **App Móvil** | Flutter Android/iOS | ✅ Desarrollada | Versión Beta |
| **Mapas** | Google Maps API | ✅ Integrado | API Key activa |

### **Recursos Humanos**

| Rol | Responsabilidad | Estado |
|-----|----------------|--------|
| Desarrollador Backend | API REST, WebSocket, Análisis Espacial | ✅ Activo |
| Desarrollador Frontend | App Flutter, UI/UX | ✅ Activo |
| Especialista GIS | PostGIS, Operaciones Espaciales | ✅ Activo |
| DevOps | Despliegue, Servidor, Nginx | 🔄 En progreso |
| Cartógrafo | Digitalización Shapefiles | ⏳ Pendiente |
| Capacitador | Entrenamiento usuarios | ⏳ Pendiente |

---

## Conclusión

La implementación de esta **aplicación SIG de monitoreo infantil** proporciona:

### **Beneficios Alcanzados:**
1. ✅ **Herramienta eficaz** para gestión de seguridad de niños preescolares
2. ✅ **Respuesta rápida** ante situaciones de riesgo mediante alertas automáticas en tiempo real
3. ✅ **Análisis espacial preciso** utilizando capacidades GIS (PostGIS)
4. ✅ **Reducción de inseguridad** al permitir monitoreo continuo
5. ✅ **Toma de decisiones tempranas** con información geográfica actualizada
6. ✅ **Sistema escalable** que puede extenderse a personas vulnerables (adultos mayores, personas con discapacidad)

### **Ventajas sobre Sistemas Tradicionales:**
- ❌ **Controles manuales**: Laboriosos, costosos, lentos
- ✅ **Monitor Infantil SIG**: Automático, económico, instantáneo

### **Impacto Esperado:**
- Prevención de pérdidas de niños en centros educativos
- Reducción de tiempo de respuesta ante incidentes
- Mayor tranquilidad para madres y tutores
- Datos históricos para análisis de patrones de movimiento
- Base tecnológica para expandir a otros grupos vulnerables

### **Capacidades SIG Destacadas:**
- Operaciones espaciales que sistemas estándar no realizan (ST_Contains, ST_Distance, ST_Area)
- Visualización geográfica intuitiva en mapas interactivos
- Almacenamiento eficiente de geometrías vectoriales (shapefiles)
- Consultas espaciales optimizadas con índices GiST
- Integración de múltiples capas de información geográfica

---

**Estado Actual del Proyecto**: En fase de despliegue y pruebas  
**Nivel de Completitud**: 75% (Backend completo, Frontend completo, Despliegue 60%)  
**Próximo Hito**: Configuración completa de WebSocket en servidor de producción  
**Fecha de Inicio**: Octubre 2025  
**Fecha Estimada de Finalización**: Diciembre 2025  

---

## Tecnologías Resumidas (Comparación con Enunciado)

| Componente Requerido | Tecnología Implementada | Cumplimiento |
|---------------------|------------------------|--------------|
| **Software SIG** | GeoDjango + PostGIS | ✅ Cumple (equivalente a ArcGIS) |
| **Base de Datos Espacial** | PostgreSQL + PostGIS | ✅ Cumple |
| **Análisis Vectorial** | PostGIS (Polygon, Point) | ✅ Cumple (Shapefiles) |
| **Aplicación Móvil** | Flutter Android/iOS | ✅ Cumple |
| **Servidor** | DigitalOcean Ubuntu | ✅ Cumple |
| **Sistema de Alertas** | WebSocket + Push Notifications | ✅ Cumple |
| **Operaciones Espaciales** | ST_Contains, ST_Distance | ✅ Cumple |
| **Mapas Interactivos** | Google Maps API | ✅ Cumple |

---

**Fecha de creación**: 5 de diciembre de 2025  
**Última actualización**: 5 de diciembre de 2025  
**Versión**: 2.0 - Alineado con enunciado académico
