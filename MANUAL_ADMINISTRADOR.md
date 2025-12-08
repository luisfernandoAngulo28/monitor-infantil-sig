# 📘 Manual del Administrador - Sistema de Monitoreo Infantil

**Versión:** 1.0  
**Fecha:** Diciembre 2025  
**Audiencia:** Administradores de centros educativos y personal técnico  

---

## 📑 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Panel de Administración Django](#panel-de-administración)
4. [Gestión de Centros Educativos](#gestión-de-centros-educativos)
5. [Gestión de Niños](#gestión-de-niños)
6. [Gestión de Tutores](#gestión-de-tutores)
7. [Monitoreo de Posiciones GPS](#monitoreo-de-posiciones-gps)
8. [Sistema de Alertas](#sistema-de-alertas)
9. [Reportes y Estadísticas](#reportes-y-estadísticas)
10. [Solución de Problemas](#solución-de-problemas)
11. [Mantenimiento](#mantenimiento)

---

## 1. Introducción

### ¿Qué es el Sistema de Monitoreo Infantil?

El Sistema de Monitoreo Infantil es una aplicación SIG (Sistema de Información Geográfica) que permite:
- 📍 Rastrear la ubicación GPS en tiempo real de niños prescolares
- 🔔 Generar alertas automáticas cuando un niño sale del área segura de su kinder
- 📱 Notificar instantáneamente a padres y tutores
- 📊 Visualizar historial de movimientos
- 🗺️ Realizar búsquedas espaciales de niños cercanos

### Roles del Administrador

Como administrador del sistema, usted puede:
- ✅ Crear y editar centros educativos (kinders)
- ✅ Definir áreas seguras mediante polígonos geográficos
- ✅ Registrar niños y asignarlos a centros
- ✅ Gestionar tutores y sus permisos
- ✅ Revisar alertas y notificaciones
- ✅ Consultar historial de posiciones GPS
- ✅ Generar reportes de incidentes

---

## 2. Acceso al Sistema

### 2.1 URL del Panel de Administración

**Producción:**
```
https://monitor-infantil.duckdns.org/admin/
```

### 2.2 Credenciales Iniciales

Las credenciales son proporcionadas por el administrador del sistema.

**Ejemplo:**
- Usuario: `admin` o `fernando`
- Contraseña: (proporcionada de forma segura)

### 2.3 Primer Acceso

1. Abra su navegador web (Chrome, Firefox, Edge)
2. Navegue a `https://monitor-infantil.duckdns.org/admin/`
3. Verá la pantalla de login de Django:

```
┌─────────────────────────────────┐
│   Django Administration         │
│                                  │
│   Usuario: [____________]       │
│   Contraseña: [____________]    │
│                                  │
│   [  Iniciar sesión  ]          │
└─────────────────────────────────┘
```

4. Ingrese sus credenciales
5. Haga clic en "Iniciar sesión"

### 2.4 Cambiar Contraseña

**IMPORTANTE:** Cambie su contraseña en el primer acceso.

1. En el panel superior derecho, haga clic en su nombre de usuario
2. Seleccione "Cambiar contraseña"
3. Ingrese contraseña actual y nueva contraseña (2 veces)
4. Haga clic en "Cambiar mi contraseña"

---

## 3. Panel de Administración Django

### 3.1 Pantalla Principal

Después de iniciar sesión, verá:

```
┌────────────────────────────────────────────────────────┐
│  Administración de Django                              │
│  Bienvenido, fernando. Cambiar contraseña / Cerrar     │
├────────────────────────────────────────────────────────┤
│                                                         │
│  AUTENTICACIÓN Y AUTORIZACIÓN                          │
│  • Usuarios                         [Agregar] [Cambiar]│
│  • Grupos                           [Agregar] [Cambiar]│
│                                                         │
│  GIS_TRACKING                                          │
│  • Centros educativos               [Agregar] [Cambiar]│
│  • Niños                            [Agregar] [Cambiar]│
│  • Posiciones GPS                   [Agregar] [Cambiar]│
│                                                         │
│  ALERTS                                                │
│  • Alertas                          [Agregar] [Cambiar]│
│  • Notificaciones Tutor             [Agregar] [Cambiar]│
│                                                         │
│  CORE                                                  │
│  • Tutores                          [Agregar] [Cambiar]│
│  • Usuarios                         [Agregar] [Cambiar]│
└────────────────────────────────────────────────────────┘
```

### 3.2 Navegación

- **Agregar:** Crear nuevo registro
- **Cambiar:** Ver/editar registros existentes
- **Eliminar:** Borrar registros (use con precaución)
- **Acciones masivas:** Aplicar cambios a múltiples registros

---

## 4. Gestión de Centros Educativos

### 4.1 Ver Centros Existentes

1. En el panel principal, haga clic en **"Cambiar"** junto a "Centros educativos"
2. Verá una lista de todos los kinders registrados:

```
Centros educativos
┌────────────────────────────────────────────────────────┐
│ Buscar: [_____________] 🔍                             │
├────┬──────────────────────┬─────────┬────────┬────────┤
│ ☑  │ Nombre               │ Código  │ Ciudad │ Activo │
├────┼──────────────────────┼─────────┼────────┼────────┤
│ ☐  │ Kinder Arco Iris     │ KASC001 │ SC     │   ✓    │
│ ☐  │ Jardín Los Patitos   │ JLPSC02 │ SC     │   ✓    │
│ ☐  │ Centro Infantil Sol  │ CISSC03 │ SC     │   ✓    │
└────┴──────────────────────┴─────────┴────────┴────────┘
```

### 4.2 Crear Nuevo Centro Educativo

1. Haga clic en **"Agregar centro educativo"**
2. Complete el formulario:

**Información Básica:**
```
Nombre: _________________________________
Código: _________________________________
Dirección: ______________________________
Ciudad: Santa Cruz de la Sierra
Departamento: Santa Cruz
Teléfono: _______________________________
Email: __________________________________
```

**Área Segura (Polígono):**

Esta es la parte más importante. El área segura define dónde el niño puede estar sin generar alertas.

**Opción A: Ingresar coordenadas manualmente**

Formato WKT (Well-Known Text):
```
POLYGON((
  -63.1821 -17.7833,
  -63.1810 -17.7833,
  -63.1810 -17.7840,
  -63.1821 -17.7840,
  -63.1821 -17.7833
))
```

**Explicación:**
- Cada línea es un punto: `longitud latitud`
- El primer y último punto deben ser iguales (cerrar el polígono)
- Mínimo 4 puntos (3 esquinas + punto de cierre)

**Opción B: Usar herramienta web (recomendado)**

1. Visite: https://geojson.io
2. Use la herramienta de dibujo para crear un polígono sobre el mapa
3. Copie las coordenadas generadas
4. Péguelas en el campo "Área segura"

**Captura de Coordenadas:**

Si necesita obtener coordenadas de Google Maps:
1. Abra Google Maps
2. Haga clic derecho en el mapa
3. Seleccione "¿Qué hay aquí?"
4. Verá las coordenadas: `-17.7833, -63.1821`
5. Formato para WKT: `-63.1821 -17.7833` (lng, lat)

3. Haga clic en **"Guardar"**

### 4.3 Editar Centro Existente

1. En la lista de centros, haga clic en el nombre del centro
2. Modifique los campos necesarios
3. Haga clic en **"Guardar"** o **"Guardar y continuar editando"**

### 4.4 Desactivar Centro

Para desactivar un centro sin eliminarlo:
1. Edite el centro
2. Desmarque la casilla **"Activo"**
3. Guarde los cambios

**NOTA:** Los niños asignados a un centro desactivado NO generarán alertas.

---

## 5. Gestión de Niños

### 5.1 Ver Niños Registrados

1. Haga clic en **"Cambiar"** junto a "Niños"
2. Verá la lista:

```
Niños
┌────────────────────────────────────────────────────────┐
│ Filtros: Centro ▼ | Tutor ▼ | Tracking Activo ▼       │
├────┬───────────────────┬──────────────┬────────────────┤
│ ☑  │ Nombre            │ Centro       │ Tutor          │
├────┼───────────────────┼──────────────┼────────────────┤
│ ☐  │ Carlos López      │ Arco Iris    │ María López    │
│ ☐  │ Sofía Pérez       │ Los Patitos  │ Ana Pérez      │
│ ☐  │ Mateo García      │ Sol          │ Juan García    │
└────┴───────────────────┴──────────────┴────────────────┘
```

### 5.2 Registrar Nuevo Niño

1. Haga clic en **"Agregar niño"**
2. Complete el formulario:

**Datos Personales:**
```
Nombre: _________________________________
Apellido paterno: _______________________
Apellido materno: _______________________
Fecha de nacimiento: [DD/MM/AAAA]
Sexo: ○ Masculino  ○ Femenino
```

**Foto (opcional):**
```
[Elegir archivo] niño_foto.jpg
```

**Centro Educativo:**
```
Centro educativo: [Seleccionar ▼]
```
Seleccione el kinder al que asiste el niño.

**Tutor Principal:**
```
Tutor principal: [Seleccionar ▼]
```
Este tutor recibirá todas las alertas.

**Tutores Adicionales (opcional):**
```
Tutores adicionales: [Seleccionar múltiples ▼]
```
Use Ctrl+Click para seleccionar varios tutores.

**Dispositivo:**
```
ID de dispositivo: _________________________
```
Este es el ID único del dispositivo móvil del niño.
Se obtiene automáticamente de la app Flutter.

**Estado:**
```
☑ Activo
☑ Tracking activo
```
- **Activo:** El niño está registrado en el sistema
- **Tracking activo:** Se monitorea su ubicación GPS

3. Haga clic en **"Guardar"**

### 5.3 Editar Información de Niño

1. Haga clic en el nombre del niño
2. Modifique los campos necesarios
3. **IMPORTANTE:** Al cambiar de centro educativo, el área segura cambia automáticamente

### 5.4 Desactivar Tracking

Para dejar de monitorear temporalmente a un niño:
1. Edite el niño
2. Desmarque **"Tracking activo"**
3. Guarde

**EFECTO:** No se registrarán posiciones GPS ni se generarán alertas.

---

## 6. Gestión de Tutores

### 6.1 Ver Tutores

1. Haga clic en **"Cambiar"** junto a "Tutores"
2. Lista de tutores registrados:

```
Tutores
┌────────────────────────────────────────────────────────┐
│ Buscar: [_____________] 🔍                             │
├────┬──────────────────┬─────────┬──────────────────────┤
│ ☑  │ Nombre           │ CI      │ Teléfono             │
├────┼──────────────────┼─────────┼──────────────────────┤
│ ☐  │ María López      │ 1234567 │ +591 7XX XXX XXX     │
│ ☐  │ Ana Pérez        │ 7654321 │ +591 7XX XXX XXX     │
└────┴──────────────────┴─────────┴──────────────────────┘
```

### 6.2 Crear Tutor

1. **IMPORTANTE:** Primero debe crear un Usuario
2. Luego vincular el Tutor al Usuario

**Paso 1: Crear Usuario**

1. Vaya a "Usuarios" (sección CORE)
2. Haga clic en "Agregar usuario"
3. Complete:
```
Nombre de usuario: maria.lopez
Contraseña: ********
Confirmar contraseña: ********
Tipo de usuario: TUTOR
Nombres: María
Apellidos: López González
Email: maria.lopez@email.com
Teléfono: +591 7XX XXX XXX
```
4. Guarde

**Paso 2: Crear Tutor**

1. Vaya a "Tutores" (sección CORE)
2. Haga clic en "Agregar tutor"
3. Complete:
```
Usuario: [Seleccionar: maria.lopez ▼]
Relación: Madre
CI: 1234567
Teléfono emergencia: +591 6XX XXX XXX
```
4. Guarde

### 6.3 Vincular Tutor con Niño

Hay 2 formas:

**Opción A: Desde el Niño**
1. Edite el niño
2. Seleccione tutor en "Tutor principal"
3. Guarde

**Opción B: Desde el Tutor**
1. Edite el tutor
2. En "Niños principal" verá la lista de niños asignados
3. Esta es solo de lectura

---

## 7. Monitoreo de Posiciones GPS

### 7.1 Ver Posiciones Recientes

1. Haga clic en **"Cambiar"** junto a "Posiciones GPS"
2. Lista ordenada por timestamp (más reciente primero):

```
Posiciones GPS
┌────────────────────────────────────────────────────────┐
│ Filtros: Niño ▼ | Dentro área ▼ | Fecha ▼             │
├──────────────┬───────────┬──────────┬────────┬────────┤
│ Niño         │ Timestamp │ Batería  │ Área   │ Ver    │
├──────────────┼───────────┼──────────┼────────┼────────┤
│ Carlos López │ 14:40:08  │ 85%      │ ✓ Sí   │ [Mapa] │
│ Sofía Pérez  │ 14:35:12  │ 92%      │ ✗ No   │ [Mapa] │
│ Mateo García │ 14:30:45  │ 65%      │ ✓ Sí   │ [Mapa] │
└──────────────┴───────────┴──────────┴────────┴────────┘
```

### 7.2 Interpretar Datos

**Campos importantes:**
- **Timestamp:** Fecha y hora de la posición
- **Ubicación:** Coordenadas GPS (Point)
- **Nivel batería:** Porcentaje de batería del dispositivo
- **Dentro área segura:** 
  - ✓ Verde: Niño dentro del kinder
  - ✗ Rojo: Niño fuera del área (ALERTA)
- **Velocidad:** Km/h (útil para detectar movimiento)
- **Precisión:** Metros de error GPS (menor es mejor)

### 7.3 Ver Posición en Mapa

1. Haga clic en el ID de la posición
2. Verá el detalle:
```
Posición GPS #6
┌────────────────────────────────────────────┐
│ Niño: Carlos López Días                    │
│ Timestamp: 2025-12-08 14:40:08             │
│ Ubicación: POINT(-122.084 37.422)          │
│                                            │
│ [Ver en mapa]                              │
│                                            │
│ Detalles:                                  │
│ • Nivel batería: 85%                       │
│ • Dentro área segura: Sí                   │
│ • Velocidad: 0.0 km/h                      │
│ • Precisión: - metros                      │
└────────────────────────────────────────────┘
```

### 7.4 Filtrar Posiciones

**Por Niño:**
1. Use el filtro "Niño" en el lateral derecho
2. Seleccione el niño deseado
3. Verá solo sus posiciones

**Por Fecha:**
1. Filtro "Fecha"
2. Seleccione "Hoy", "Últimos 7 días", etc.

**Por Estado:**
1. Filtro "Dentro área segura"
2. "Sí" = Solo posiciones seguras
3. "No" = Solo posiciones fuera del área (incidentes)

---

## 8. Sistema de Alertas

### 8.1 ¿Qué es una Alerta?

Una alerta se genera automáticamente cuando:
1. El niño sale del área segura de su kinder
2. El sistema detecta una anomalía en la posición GPS
3. La batería del dispositivo está críticamente baja

### 8.2 Ver Alertas

1. Haga clic en **"Cambiar"** junto a "Alertas"
2. Lista de alertas:

```
Alertas
┌────────────────────────────────────────────────────────┐
│ Filtros: Niño ▼ | Tipo ▼ | Estado ▼                   │
├──────┬────────────┬──────────┬─────────┬──────────────┤
│ Niño │ Tipo       │ Fecha    │ Estado  │ Acciones     │
├──────┼────────────┼──────────┼─────────┼──────────────┤
│ Sofía│ SALIDA     │ 14:35:12 │ ENVIADA │ [Resolver]   │
│ Mateo│ BATERÍA    │ 14:20:05 │ LEÍDA   │ [Resolver]   │
│ Carlos│ SALIDA    │ 12:10:30 │ RESUELTA│ [Ver]        │
└──────┴────────────┴──────────┴─────────┴──────────────┘
```

### 8.3 Tipos de Alerta

- **SALIDA:** Niño salió del área segura
- **BATERÍA_BAJA:** Batería < 20%
- **SIN_SEÑAL:** No hay actualizaciones GPS > 30 min

### 8.4 Estados de Alerta

1. **PENDIENTE:** Alerta creada, notificación no enviada
2. **ENVIADA:** Notificación enviada a tutores
3. **LEÍDA:** Tutor vio la alerta
4. **RESUELTA:** Incidente resuelto

### 8.5 Resolver Alerta

1. Haga clic en la alerta
2. Revise los detalles:
```
Alerta #5 - SALIDA DE ÁREA SEGURA
┌────────────────────────────────────────────┐
│ Niño: Sofía Pérez                          │
│ Fecha creación: 2025-12-08 14:35:12        │
│ Estado: ENVIADA                            │
│                                            │
│ Mensaje:                                   │
│ "Sofía Pérez ha salido del área segura    │
│  del Jardín Los Patitos"                   │
│                                            │
│ Posición GPS: [Ver en mapa]               │
│ Coordenadas: -17.7850, -63.1805            │
│                                            │
│ Notificaciones enviadas:                   │
│ • Ana Pérez (Madre) - Enviado 14:35:13    │
│ • Pedro Pérez (Padre) - Enviado 14:35:13  │
│                                            │
│ [Marcar como resuelta]                     │
└────────────────────────────────────────────┘
```

3. Si el incidente fue resuelto, haga clic en **"Marcar como resuelta"**
4. Opcionalmente agregue un comentario

### 8.6 Notificaciones a Tutores

Las notificaciones se envían automáticamente via:
- 📱 **Push notification** (Firebase Cloud Messaging)
- 📧 **Email** (si está configurado)

**Estado de notificaciones:**
1. Haga clic en "Notificaciones Tutor"
2. Verá:
```
Notificaciones Tutor
┌────────────────────────────────────────────────────────┐
│ Tutor       │ Alerta │ Enviado     │ Leído     │ Estado│
├─────────────┼────────┼─────────────┼───────────┼───────┤
│ Ana Pérez   │ #5     │ 14:35:13 ✓  │ 14:36:20  │ LEÍDA │
│ María López │ #4     │ 12:10:31 ✓  │ -         │ENVIADA│
└─────────────┴────────┴─────────────┴───────────┴───────┘
```

---

## 9. Reportes y Estadísticas

### 9.1 Reportes Disponibles

**Desde el Admin:**

1. **Historial de Posiciones por Niño**
   - Filtrar por niño
   - Exportar a CSV
   - Ver en mapa

2. **Alertas por Período**
   - Filtrar por fecha
   - Tipo de alerta
   - Estado

3. **Estadísticas de Uso**
   - Niños activos
   - Alertas por centro
   - Promedio de tiempo de respuesta

### 9.2 Exportar Datos

1. Seleccione múltiples registros (marque checkboxes)
2. En "Acción" seleccione "Exportar como CSV"
3. Haga clic en "Ir"
4. Se descargará un archivo Excel/CSV

### 9.3 API REST (para desarrolladores)

**Endpoints disponibles:**

```bash
# Obtener niños
GET https://monitor-infantil.duckdns.org/api/ninos/

# Posiciones GPS
GET https://monitor-infantil.duckdns.org/api/posiciones/

# Alertas
GET https://monitor-infantil.duckdns.org/api/alertas/

# Búsqueda cercanos
GET https://monitor-infantil.duckdns.org/api/busqueda-cercanos/ninos-cercanos/{lat}/{lng}/?radius=5000
```

**Autenticación:**
Requiere token JWT. Ver documentación técnica.

---

## 10. Solución de Problemas

### 10.1 No Aparecen Posiciones GPS

**Problema:** El niño tiene tracking activo pero no se registran posiciones.

**Soluciones:**
1. Verificar que la app móvil esté abierta
2. Revisar permisos de ubicación en el dispositivo
3. Verificar conexión a internet
4. Comprobar que `dispositivo_id` esté configurado correctamente

**Verificación:**
```bash
# En el servidor (SSH)
python manage.py shell
>>> from apps.gis_tracking.models import Nino, PosicionGPS
>>> nino = Nino.objects.get(nombre="Carlos")
>>> PosicionGPS.objects.filter(nino=nino).count()
6  # Debe ser > 0
```

### 10.2 Alertas No Se Envían

**Problema:** Se genera alerta pero no llega notificación a tutores.

**Causas posibles:**
1. Tutor no tiene `firebase_token` configurado
2. Firebase no está configurado correctamente
3. Email no configurado

**Verificación:**
```sql
-- Ver tokens Firebase de tutores
SELECT u.username, u.firebase_token
FROM core_usuario u
WHERE tipo_usuario = 'TUTOR';
```

**Solución:**
1. Tutor debe abrir la app Flutter al menos una vez
2. La app registrará el token automáticamente

### 10.3 Área Segura No Detecta Correctamente

**Problema:** Niño está dentro del kinder pero genera alerta de salida.

**Causa:** El polígono del área segura está mal definido.

**Verificación:**
1. Edite el centro educativo
2. Copie las coordenadas del "Área segura"
3. Péguelas en https://geojson.io
4. Verifique que el polígono cubra todo el kinder

**Solución:**
1. Redibuje el polígono en geojson.io
2. Asegúrese de:
   - Cubrir todo el edificio
   - Incluir áreas de juego
   - Agregar margen de seguridad (5-10 metros)
3. Copie el nuevo polígono
4. Actualice en el admin

### 10.4 Error 500 en Admin

**Problema:** Al intentar acceder a Posiciones GPS sale error 500.

**Causa:** Falta extensión PostGIS o migración no aplicada.

**Solución (requiere acceso SSH):**
```bash
cd /opt/monitor-infantil-sig/backend
source venv/bin/activate
python manage.py migrate
supervisorctl restart monitor-infantil-daphne
```

### 10.5 Lentitud en el Sistema

**Problema:** El admin Django responde lento.

**Soluciones:**
1. Aplicar índices espaciales:
```bash
python manage.py shell
>>> from django.db import connection
>>> cursor = connection.cursor()
>>> cursor.execute("REINDEX INDEX gis_tracking_posiciongps_ubicacion_idx;")
```

2. Limpiar posiciones antiguas (> 30 días):
```python
from apps.gis_tracking.models import PosicionGPS
from datetime import timedelta
from django.utils import timezone

fecha_limite = timezone.now() - timedelta(days=30)
PosicionGPS.objects.filter(timestamp__lt=fecha_limite).delete()
```

---

## 11. Mantenimiento

### 11.1 Tareas Diarias

- [ ] Revisar alertas pendientes (5 min)
- [ ] Verificar que todos los niños activos tengan posiciones recientes (5 min)
- [ ] Revisar log de errores (opcional)

### 11.2 Tareas Semanales

- [ ] Generar reporte de alertas de la semana
- [ ] Verificar batería promedio de dispositivos
- [ ] Actualizar información de centros si hubo cambios

### 11.3 Tareas Mensuales

- [ ] Limpiar posiciones GPS antiguas (> 30 días)
- [ ] Revisar tutores sin token Firebase
- [ ] Actualizar áreas seguras si hubo cambios estructurales
- [ ] Generar estadísticas mensuales

### 11.4 Backups

**IMPORTANTE:** Los backups son automáticos en DigitalOcean.

**Frecuencia:** Diario  
**Retención:** 7 días

**Restaurar backup:**
1. Contactar al administrador del sistema
2. Se puede restaurar cualquier backup de los últimos 7 días

### 11.5 Actualización del Sistema

**NO intente actualizar el sistema sin coordinación.**

Contacte al equipo técnico para:
- Actualizaciones de Django
- Cambios en la estructura de base de datos
- Nuevas funcionalidades
- Parches de seguridad

---

## 📞 Soporte Técnico

**Para problemas no resueltos en este manual:**

**Email:** soporte@monitor-infantil.com  
**Teléfono:** +591 XXX XXX XXX  
**Horario:** Lunes a Viernes, 8:00 - 18:00

**Información a proporcionar:**
1. Descripción del problema
2. Pasos para reproducirlo
3. Capturas de pantalla (si es posible)
4. Hora y fecha del incidente
5. Usuario afectado

---

## 📚 Recursos Adicionales

- **Manual de Usuario (Tutores):** `MANUAL_USUARIO.md`
- **Documentación Técnica:** `DOCUMENTACION_TECNICA.md`
- **FAQ:** `FAQ.md`
- **API Documentation:** https://monitor-infantil.duckdns.org/api/docs/

---

**Versión del documento:** 1.0  
**Última actualización:** Diciembre 2025  
**Autor:** Sistema de Monitoreo Infantil - INF442-SA
