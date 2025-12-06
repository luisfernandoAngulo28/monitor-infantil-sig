# Guía de Configuración - Desarrollo Local vs Producción

## Desarrollo Local

### 1. Instalar PostgreSQL + PostGIS
```bash
# Windows: Descargar PostgreSQL desde postgresql.org
# Durante la instalación, asegúrate de instalar PostGIS

# Verificar instalación
psql --version
```

### 2. Crear base de datos local
```sql
-- Conectar a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE monitor_infantil_db;

-- Conectar a la base de datos
\c monitor_infantil_db

-- Habilitar PostGIS
CREATE EXTENSION postgis;

-- Verificar
SELECT PostGIS_version();
```

### 3. Configurar entorno local
```bash
# Copiar archivo de configuración local
cp .env.local .env

# O crear un .env con estas variables:
# DEBUG=True
# DATABASE_HOST=localhost
# DATABASE_USER=postgres
# DATABASE_PASSWORD=postgres
```

### 4. Ejecutar migraciones
```bash
python manage.py migrate
```

### 5. Crear superusuario
```bash
python manage.py createsuperuser
```

### 6. Crear datos de prueba
```bash
python manage.py shell
```

```python
from apps.core.models import Usuario, Tutor
from apps.gis_tracking.models import CentroEducativo, Nino
from django.contrib.gis.geos import Point, Polygon

# Crear usuarios de prueba
maria = Usuario.objects.create_user(
    username='maria.lopez',
    password='demo123456',
    email='maria@test.com',
    first_name='María',
    last_name='López',
    tipo_usuario='TUTOR'
)

# Crear tutor
tutor = Tutor.objects.create(
    usuario=maria,
    relacion='MADRE',
    ci='1234567',
    telefono_emergencia='70000000'
)

# Crear centro educativo
coords = [
    (-63.1812, -17.7833),  # lng, lat
    (-63.1812, -17.7843),
    (-63.1822, -17.7843),
    (-63.1822, -17.7833),
    (-63.1812, -17.7833)
]
area = Polygon(coords)

centro = CentroEducativo.objects.create(
    nombre='Kinder Test',
    codigo='KT001',
    direccion='Calle Test 123',
    telefono='3000000',
    ubicacion_centro=Point(-63.1817, -17.7838),
    area_segura=area,
    margen_metros=50
)

# Crear niño
nino = Nino.objects.create(
    nombre='Juan',
    apellido_paterno='Pérez',
    fecha_nacimiento='2020-01-15',
    sexo='M',
    centro_educativo=centro,
    tutor_principal=tutor,
    tracking_activo=True
)

print(f"✅ Datos creados: {nino.nombre_completo}")
```

### 7. Ejecutar servidor local
```bash
python manage.py runserver 0.0.0.0:8000
```

### 8. Ejecutar app Flutter
```bash
cd mobile/monitor_infantil_app
flutter run
```

## Producción - DigitalOcean

### Configurar variables de entorno
```bash
# En el servidor
cp .env.production .env
nano .env

# Cambiar:
# - SECRET_KEY por un valor seguro
# - DEBUG=False
# - Credenciales de base de datos DigitalOcean
```

### Ejecutar con Gunicorn
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Cambiar entre entornos

### Flutter: Editar api_config.dart
```dart
// LOCAL
static const String baseUrl = 'http://10.0.2.2:8000';

// PRODUCCIÓN
static const String baseUrl = 'http://143.198.30.170:8000';
```

### Django: Cambiar archivo .env
```bash
# LOCAL
cp .env.local .env

# PRODUCCIÓN
cp .env.production .env
```
