# Tutorial de Uso - Monitor Infantil SIG

## 📚 Guía Paso a Paso

### 1️⃣ Configuración Inicial

#### Paso 1: Crear Centro Educativo (Kinder)

1. Ir al panel de administración: http://localhost:8000/admin
2. Navegar a **GIS Tracking → Centros Educativos**
3. Click en **Agregar Centro Educativo**
4. Completar datos:
   - **Nombre**: Kinder Los Pitufos
   - **Código**: KP001
   - **Dirección**: Av. San Martin #123
   - **Teléfono**: 3-3456789

5. **Dibujar el Área Segura** (Polígono):
   - En el mapa, usar las herramientas de dibujo
   - Seleccionar "Dibujar Polígono"
   - Click en el mapa para marcar los vértices del área del kinder
   - Doble click para cerrar el polígono
   - El polígono debe cubrir completamente el área del kinder

6. Guardar

#### Paso 2: Registrar Tutor

1. **Crear Usuario** primero:
   - Ir a **Core → Usuarios**
   - Agregar usuario con:
     - Username: maria_gonzalez
     - Email: maria@example.com
     - Tipo de usuario: **Tutor/Madre/Padre**
     - Teléfono: 70123456

2. **Crear Perfil de Tutor**:
   - Ir a **Core → Tutores**
   - Seleccionar el usuario creado
   - Relación: Madre
   - CI: 12345678 SC
   - Teléfono emergencia: 70123456

#### Paso 3: Registrar Niño

1. Ir a **GIS Tracking → Niños/as**
2. Click en **Agregar Niño/a**
3. Completar datos:
   - Nombre: Pedrito
   - Apellido Paterno: González
   - Fecha de Nacimiento: 15/05/2020
   - Sexo: Masculino
   - **Centro Educativo**: Seleccionar el kinder creado
   - **Tutor Principal**: Seleccionar el tutor creado
   - **Dispositivo ID**: device_pedrito_001
   - **Tracking Activo**: ✅ Marcado

4. Guardar

---

### 2️⃣ Uso de la API para Tracking GPS

#### Obtener Token de Autenticación

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria_gonzalez",
    "password": "tu_password"
  }'
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Guardar el `access` token.

#### Registrar Posición GPS (desde app móvil)

**Posición DENTRO del área:**
```bash
curl -X POST http://localhost:8000/api/ninos/1/registrar_posicion/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "latitud": -17.7835,
    "longitud": -63.1815,
    "precision_metros": 10.5,
    "nivel_bateria": 85
  }'
```

**Posición FUERA del área (genera alerta):**
```bash
curl -X POST http://localhost:8000/api/ninos/1/registrar_posicion/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "latitud": -17.7900,
    "longitud": -63.1900,
    "precision_metros": 8.0,
    "nivel_bateria": 80
  }'
```

#### Consultar Estado del Niño

```bash
curl -X GET http://localhost:8000/api/ninos/1/estado/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

Respuesta:
```json
{
  "nino": {
    "id": 1,
    "nombre_completo": "Pedrito González",
    "edad": 4,
    ...
  },
  "ultima_posicion": {
    "geometry": {
      "coordinates": [-63.1815, -17.7835]
    },
    "properties": {
      "dentro_area_segura": true,
      "nivel_bateria": 85
    }
  },
  "dentro_area_segura": true,
  "alertas_activas": 0
}
```

---

### 3️⃣ Gestión de Alertas

#### Ver Mis Alertas (como Tutor)

```bash
curl -X GET http://localhost:8000/api/mis-alertas/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

#### Marcar Alerta como Leída

```bash
curl -X POST http://localhost:8000/api/alertas/1/marcar_leida/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

#### Resolver Alerta

```bash
curl -X POST http://localhost:8000/api/alertas/1/resolver/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

---

### 4️⃣ Panel Web de Monitoreo

#### Dashboard

Visitar: http://localhost:8000/

Muestra:
- Total de niños registrados
- Cuántos están dentro del área
- Alertas activas
- Alertas recientes

#### Mapa en Tiempo Real

Visitar: http://localhost:8000/mapa/

Muestra:
- Polígonos de áreas seguras (azul)
- Posiciones GPS de niños:
  - 🟢 Verde: Dentro del área
  - 🔴 Rojo: Fuera del área
- Lista lateral con todos los niños

---

### 5️⃣ Configuración de Notificaciones Push

#### Actualizar Token de Firebase (desde app móvil)

```bash
curl -X POST http://localhost:8000/api/configuracion/actualizar_firebase_token/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "firebase_token": "fcm_token_del_dispositivo..."
  }'
```

Cuando el niño salga del área, el tutor recibirá una notificación push automáticamente.

---

### 6️⃣ Escenarios de Prueba

#### Escenario 1: Niño Sale del Área

1. Registrar posición FUERA del polígono
2. El sistema automáticamente:
   - Marca `dentro_area_segura = False`
   - Crea una **Alerta** de tipo `SALIDA_AREA`
   - Envía notificación push a todos los tutores
3. Verificar en `/admin/alerts/alerta/`
4. Verificar en API `/api/mis-alertas/`

#### Escenario 2: Niño Regresa al Área

1. Registrar posición DENTRO del polígono
2. El sistema marca `dentro_area_segura = True`
3. NO genera nueva alerta
4. Tutor puede resolver la alerta anterior

#### Escenario 3: Historial de Movimiento

```bash
# Ver últimas 24 horas
curl -X GET "http://localhost:8000/api/ninos/1/historial/?dias=1" \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

---

### 7️⃣ Análisis Espacial

El sistema usa **GeoDjango** para:

1. **Point-in-Polygon**: Detectar si niño está dentro del área
2. **Centroid**: Calcular centro del kinder automáticamente
3. **Buffer**: Aplicar margen de tolerancia (opcional)
4. **Distance**: Calcular distancia al centro

Ejemplo en código:
```python
# En PosicionGPS.save()
area_kinder = self.nino.centro_educativo.area_segura
self.dentro_area_segura = area_kinder.contains(self.ubicacion)
```

---

### 8️⃣ Ejecución de Tests

```bash
python manage.py test apps.api.tests
```

Tests incluidos:
- ✅ Registrar posición dentro del área
- ✅ Registrar posición fuera (genera alerta)
- ✅ Obtener estado del niño
- ✅ Historial de posiciones
- ✅ Mis alertas

---

### 9️⃣ Comandos Útiles

```bash
# Crear datos de prueba
python manage.py shell
>>> from apps.core.models import *
>>> from apps.gis_tracking.models import *

# Ver todas las posiciones
python manage.py shell
>>> PosicionGPS.objects.all()

# Ver alertas
>>> Alerta.objects.filter(estado='PENDIENTE')

# Limpiar posiciones antiguas (más de 30 días)
>>> from datetime import timedelta
>>> from django.utils import timezone
>>> fecha_limite = timezone.now() - timedelta(days=30)
>>> PosicionGPS.objects.filter(timestamp__lt=fecha_limite).delete()
```

---

## 📱 Próximos Pasos: App Móvil

Para la app móvil (Flutter recomendado):

1. **Obtener ubicación GPS** en tiempo real
2. **Enviar cada 30 segundos** a `/api/ninos/{id}/registrar_posicion/`
3. **Escuchar notificaciones** Firebase Cloud Messaging
4. **Mostrar alertas** en la app

Ejemplo Flutter:
```dart
// Obtener ubicación
Position position = await Geolocator.getCurrentPosition();

// Enviar a API
await http.post(
  Uri.parse('http://tu-servidor/api/ninos/1/registrar_posicion/'),
  headers: {'Authorization': 'Bearer $token'},
  body: json.encode({
    'latitud': position.latitude,
    'longitud': position.longitude,
    'nivel_bateria': batteryLevel,
  }),
);
```

¡Listo! 🎉
