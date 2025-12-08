# Integración Traccar GPS - Guía Completa

## 📋 Descripción

Este proyecto ahora incluye integración completa con **Traccar GPS Server**, permitiendo rastrear dispositivos móviles con Traccar Client en tiempo real. Los padres/tutores pueden registrar a sus hijos en la app móvil y vincularlos con sus dispositivos GPS.

## 🏗️ Arquitectura

```
┌──────────────────┐
│  Traccar Client  │ (App móvil en teléfono del niño)
│   Android/iOS    │
└────────┬─────────┘
         │ HTTP POST (Protocolo OsmAnd)
         ↓
┌──────────────────┐
│  Traccar Server  │ Puerto 5055 (GPS)
│    (Docker)      │ Puerto 8082 (Web/API)
└────────┬─────────┘
         │ Webhook POST → http://backend:8000/api/traccar/webhook/
         ↓
┌──────────────────────────────────────┐
│         Django Backend               │
│  ┌──────────────────────────────┐   │
│  │ Webhook Endpoint             │   │
│  │ /api/traccar/webhook/        │   │
│  └──────────┬───────────────────┘   │
│             ↓                        │
│  ┌──────────────────────────────┐   │
│  │ PosicionGPS Model            │   │
│  │ - Auto Point-in-Polygon      │   │
│  │ - Alert generation           │   │
│  └──────────┬───────────────────┘   │
│             ↓                        │
│  ┌──────────────────────────────┐   │
│  │ WebSocket Consumer           │   │
│  │ Broadcast to tutors          │   │
│  └──────────────────────────────┘   │
└──────────────────────────────────────┘
         │
         ↓
┌──────────────────┐
│  Flutter App     │ (Teléfono del padre/tutor)
│  Real-time Map   │
└──────────────────┘
```

## 🚀 Paso 1: Iniciar Traccar Server

### Opción A: Docker Compose (Recomendado)

```bash
cd backend
docker-compose -f docker-compose.traccar.yml up -d
```

### Opción B: Con docker-compose principal

```bash
cd backend
docker-compose up -d
docker-compose -f docker-compose.traccar.yml up -d
```

### Verificar que Traccar está corriendo

```bash
docker ps | grep traccar
```

Deberías ver el contenedor `traccar_server` corriendo en:

- **Puerto 8082**: Web UI & REST API
- **Puerto 5055**: Protocolo GPS (OsmAnd)

## 🌐 Paso 2: Acceder a Traccar Web UI

1. Abrir navegador: `http://localhost:8082`
2. Login con credenciales por defecto:

   - **Usuario**: `admin`
   - **Contraseña**: `admin`

3. **IMPORTANTE**: Cambiar contraseña en producción:
   - Ir a Settings → Users → admin → Edit
   - Cambiar password
   - Actualizar `.env`: `TRACCAR_PASSWORD=nueva_contraseña`

## 📱 Paso 3: Instalar Traccar Client

### En el teléfono del NIÑO:

#### Android

1. Ir a Google Play Store
2. Buscar **"Traccar Client"**
3. Descargar e instalar
4. O descargar APK desde: https://www.traccar.org/client/

#### iOS

1. Ir a App Store
2. Buscar **"Traccar Client"**
3. Descargar e instalar

## ⚙️ Paso 4: Configurar Traccar Client

### En el teléfono del niño, abrir Traccar Client:

1. **Device Identifier (ID del Dispositivo)**:

   - Opción 1: Usar IMEI del teléfono (automático)
   - Opción 2: Crear ID personalizado (ej: `hijo1-samsung-2024`)
   - **IMPORTANTE**: Copiar o anotar este ID

2. **Server URL**:

   - **Desarrollo local**: `http://TU_IP_LOCAL:5055`
   - **Producción**: `http://TU_DOMINIO:5055`
   - Ejemplo: `http://192.168.1.100:5055`

3. **Location Accuracy**: High (Alta precisión)

4. **Frequency**: 30 segundos (o según preferencia)

5. **Start tracking**: Activar

### Permisos necesarios:

- ✅ Ubicación (Location) - Siempre/Always
- ✅ Ejecutar en segundo plano (Background)
- ✅ Ignorar optimización de batería (opcional pero recomendado)

## 👨‍👩‍👧‍👦 Paso 5: Registrar Hijo en la App Móvil

### En la app móvil del PADRE/TUTOR:

1. Abrir la app Monitor Infantil
2. Login con tus credenciales
3. Ir a **"Registrar Hijo/a"** (botón ➕ o en menú)
4. Completar formulario:

   - **Nombre**: Juan Carlos
   - **Apellido Paterno**: García
   - **Apellido Materno**: López (opcional)
   - **Fecha de Nacimiento**: Seleccionar del calendario
   - **Sexo**: Masculino/Femenino
   - **ID del Dispositivo (IMEI)**: Pegar el ID del Traccar Client
   - **Activar Tracking GPS**: ✅ ON

5. Presionar **"Registrar Hijo/a"**

### ¿Qué sucede detrás de escena?

1. La app envía `POST /api/ninos/` al backend Django
2. Django crea el registro del niño en la base de datos
3. Django llama a `TraccarService.register_device()`
4. Se registra automáticamente el dispositivo en Traccar Server
5. Traccar comienza a recibir posiciones GPS del Traccar Client
6. Webhook envía cada posición a Django → `POST /api/traccar/webhook/`
7. Django crea `PosicionGPS`, verifica geofencing, genera alertas
8. WebSocket envía actualización en tiempo real al padre/tutor

## 🗺️ Paso 6: Ver Ubicación en Tiempo Real

### En la app móvil del padre:

1. Ir a la pantalla de **Mapa**
2. Deberías ver un marcador con la ubicación actual de tu hijo
3. El marcador se actualiza automáticamente cada 30 segundos
4. Color del marcador:
   - 🟢 **Verde**: Dentro del área segura (kinder)
   - 🔴 **Rojo**: Fuera del área segura (alerta generada)

## 🔄 Sincronización Traccar → Django

Existen **2 métodos** de sincronización (se pueden usar ambos simultáneamente):

### Método 1: Webhook (Tiempo Real) - RECOMENDADO

Ya configurado en `backend/traccar/config/traccar.xml`:

```xml
<entry key='forward.enable'>true</entry>
<entry key='forward.url'>http://backend:8000/api/traccar/webhook/</entry>
<entry key='forward.header'>Authorization: Bearer my-super-secret-webhook-token-123456</entry>
```

- ✅ **Ventaja**: Actualización instantánea (0-2 segundos)
- ⚠️ **Requisito**: Traccar Server debe poder alcanzar Django backend

### Método 2: Polling (Respaldo)

Ejecutar comando de sincronización manual:

```bash
# Una sola vez
python manage.py sync_traccar --once

# Polling continuo cada 30 segundos
python manage.py sync_traccar --continuous --interval 30

# Polling cada 60 segundos
python manage.py sync_traccar --continuous --interval 60
```

Para ejecutar en background (producción):

```bash
# Usando screen
screen -S traccar-sync
python manage.py sync_traccar --continuous
# Presionar Ctrl+A, D para detach

# Usando nohup
nohup python manage.py sync_traccar --continuous > logs/traccar-sync.log 2>&1 &
```

## 📊 Verificar Funcionamiento

### 1. Ver logs de Traccar

```bash
docker logs -f traccar_server
```

Deberías ver mensajes como:

```
2025-12-07 10:30:15 INFO: [device-id] position received
```

### 2. Ver logs de Django

```bash
docker logs -f backend
```

Busca mensajes:

```
✅ Webhook procesado: Juan Carlos García - Posición ID 123
📍 Posición sincronizada: Juan Carlos García - (-17.782718, -63.202728) - 🟢 Seguro
```

### 3. Verificar en base de datos

```bash
python manage.py shell
```

```python
from apps.gis_tracking.models import PosicionGPS, Nino

# Ver último niño registrado
nino = Nino.objects.last()
print(f"Niño: {nino.nombre_completo()}")
print(f"Dispositivo: {nino.dispositivo_id}")

# Ver últimas posiciones
posiciones = PosicionGPS.objects.filter(nino=nino).order_by('-timestamp')[:5]
for pos in posiciones:
    print(f"{pos.timestamp}: ({pos.ubicacion.y}, {pos.ubicacion.x}) - {'✅' if pos.dentro_area_segura else '❌'}")
```

### 4. Probar webhook manualmente

```bash
curl -X POST http://localhost:8000/api/traccar/webhook/ \
  -H "Authorization: Bearer my-super-secret-webhook-token-123456" \
  -H "Content-Type: application/json" \
  -d '{
    "position": {
      "deviceTime": "2025-12-07T10:30:00.000Z",
      "latitude": -17.7833,
      "longitude": -63.1812,
      "speed": 0.0,
      "altitude": 420.5,
      "accuracy": 10.0,
      "attributes": {
        "batteryLevel": 85.0
      }
    },
    "device": {
      "id": 1,
      "uniqueId": "test-device-001",
      "name": "Test Device"
    }
  }'
```

## 🔧 APIs Disponibles

### Backend REST API

#### Registrar Niño

```bash
POST /api/ninos/
Authorization: Bearer {token}
Content-Type: application/json

{
  "nombre": "Juan Carlos",
  "apellido_paterno": "García",
  "apellido_materno": "López",
  "fecha_nacimiento": "2018-05-15",
  "sexo": "M",
  "centro_educativo": 1,
  "dispositivo_id": "862104056214397",
  "tracking_activo": true
}
```

#### Actualizar Dispositivo del Niño

```bash
PATCH /api/ninos/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
  "dispositivo_id": "nuevo-imei-123456",
  "tracking_activo": true
}
```

#### Desvincular Dispositivo

```bash
POST /api/ninos/{id}/desvincular_dispositivo/
Authorization: Bearer {token}
```

#### Listar Mis Niños

```bash
GET /api/configuracion/mis_ninos/
Authorization: Bearer {token}
```

#### Ver Estado de Niño

```bash
GET /api/ninos/{id}/estado/
Authorization: Bearer {token}
```

Respuesta:

```json
{
  "nino": {
    "id": 1,
    "nombre_completo": "Juan Carlos García López"
  },
  "ultima_posicion": {
    "latitud": -17.7833,
    "longitud": -63.1812,
    "timestamp": "2025-12-07T10:30:00Z",
    "nivel_bateria": 85
  },
  "dentro_area_segura": true,
  "alertas_activas": 0
}
```

## 🛠️ Troubleshooting

### Problema: No aparece ubicación en el mapa

**Soluciones**:

1. Verificar que Traccar Client esté enviando datos:

   - Abrir Traccar Web UI: `http://localhost:8082`
   - Ver "Devices" → Debe aparecer tu dispositivo
   - Ver "Latest" → Debe mostrar última posición

2. Verificar logs de webhook:

   ```bash
   docker logs backend | grep traccar
   ```

3. Ejecutar sincronización manual:
   ```bash
   python manage.py sync_traccar --once
   ```

### Problema: Error 401 en webhook

**Causa**: Token de autenticación incorrecto

**Solución**:

1. Verificar en `backend/.env`:

   ```
   TRACCAR_WEBHOOK_SECRET=my-super-secret-webhook-token-123456
   ```

2. Verificar en `backend/traccar/config/traccar.xml`:

   ```xml
   <entry key='forward.header'>Authorization: Bearer my-super-secret-webhook-token-123456</entry>
   ```

3. Reiniciar Traccar:
   ```bash
   docker-compose -f docker-compose.traccar.yml restart
   ```

### Problema: Dispositivo no se registra en Traccar

**Solución**:

1. Verificar conectividad:

   ```bash
   curl http://localhost:8082/api/server
   ```

2. Verificar credenciales en `.env`:

   ```
   TRACCAR_USERNAME=admin
   TRACCAR_PASSWORD=admin
   ```

3. Probar login manual:
   ```bash
   curl -X POST http://localhost:8082/api/session \
     -d "email=admin&password=admin"
   ```

### Problema: Traccar Client no envía ubicación

**Soluciones**:

1. Verificar permisos de ubicación (Always/Siempre)
2. Desactivar optimización de batería para Traccar Client
3. Verificar Server URL en Traccar Client
4. Probar con otro intervalo (60 segundos)
5. Ver logs en Traccar Client (Settings → Status)

## 📚 Recursos Adicionales

- **Documentación Traccar**: https://www.traccar.org/documentation/
- **API Reference**: https://www.traccar.org/api-reference/
- **Protocolos soportados**: https://www.traccar.org/protocols/
- **Traccar Client GitHub**: https://github.com/traccar/traccar-client-android

## 🔐 Seguridad en Producción

### 1. Cambiar credenciales de Traccar

```bash
# En Traccar Web UI
Settings → Users → admin → Edit Password
```

Actualizar `.env`:

```
TRACCAR_PASSWORD=contraseña-super-segura-123
```

### 2. Cambiar token del webhook

Generar token seguro:

```bash
openssl rand -hex 32
```

Actualizar `.env`:

```
TRACCAR_WEBHOOK_SECRET=tu-token-generado-aqui
```

Actualizar `traccar.xml`:

```xml
<entry key='forward.header'>Authorization: Bearer tu-token-generado-aqui</entry>
```

### 3. Configurar HTTPS

Para producción, configurar Nginx con SSL:

```nginx
server {
    listen 443 ssl;
    server_name gps.tudominio.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8082;
    }
}
```

Actualizar Server URL en Traccar Client:

```
https://gps.tudominio.com
```

## 🎯 Próximos Pasos

1. ✅ Traccar Server instalado y configurado
2. ✅ Traccar Client instalado en teléfono del niño
3. ✅ Hijo registrado en app móvil con dispositivo_id
4. ✅ Ubicación visible en mapa en tiempo real
5. 🔄 Configurar alertas personalizadas (próxima versión)
6. 🔄 Historial de rutas (próxima versión)
7. 🔄 Geofencing personalizado por niño (próxima versión)

## 💡 Tips

- **Batería**: Traccar Client consume batería. Recomendar cargar el teléfono del niño diariamente.
- **Datos móviles**: Asegurar que el teléfono del niño tenga plan de datos activo.
- **Precisión GPS**: Mejor precisión en exteriores. En interiores puede ser menos preciso.
- **Frecuencia**: 30 segundos es un buen balance entre precisión y batería.

## 📞 Soporte

Si tienes problemas, verifica:

1. Logs de Docker: `docker logs traccar_server`
2. Logs de Django: `docker logs backend`
3. Estado de servicios: `docker ps`
4. Conectividad de red entre contenedores

---

**Última actualización**: Diciembre 7, 2025
