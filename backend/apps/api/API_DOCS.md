"""
Documentación de la API REST - Monitor Infantil SIG

## Autenticación

Todas las peticiones requieren autenticación JWT.

### Obtener Token
POST /api/token/
Body: {
    "username": "usuario",
    "password": "password"
}

Response: {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

### Refrescar Token
POST /api/token/refresh/
Body: {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

### Headers
Authorization: Bearer {access_token}

---

## Endpoints de Niños

### Listar niños
GET /api/ninos/

### Detalle de niño
GET /api/ninos/{id}/

### Estado actual del niño
GET /api/ninos/{id}/estado/

Response: {
    "nino": {...},
    "ultima_posicion": {...},
    "dentro_area_segura": true,
    "alertas_activas": 0,
    "nivel_bateria": 85
}

### Historial de posiciones
GET /api/ninos/{id}/historial/?dias=1

### Registrar posición GPS
POST /api/ninos/{id}/registrar_posicion/
Body: {
    "latitud": -17.7833,
    "longitud": -63.1812,
    "precision_metros": 10.5,
    "nivel_bateria": 85
}

---

## Endpoints de Alertas

### Listar alertas
GET /api/alertas/

### Mis alertas (tutor autenticado)
GET /api/mis-alertas/

### Marcar alerta como leída
POST /api/alertas/{id}/marcar_leida/

### Resolver alerta
POST /api/alertas/{id}/resolver/

---

## Endpoints de Configuración

### Actualizar token Firebase
POST /api/configuracion/actualizar_firebase_token/
Body: {
    "firebase_token": "fcm_token..."
}

### Mis niños (tutor autenticado)
GET /api/configuracion/mis_ninos/

---

## Centros Educativos

### Listar centros
GET /api/centros/

### Detalle de centro
GET /api/centros/{id}/

Response incluye área segura (polígono GeoJSON)

---

## Posiciones GPS

### Listar posiciones recientes
GET /api/posiciones/

### Filtrar por niño
GET /api/posiciones/?nino={id}

### Filtrar por estado
GET /api/posiciones/?dentro_area_segura=false
"""
