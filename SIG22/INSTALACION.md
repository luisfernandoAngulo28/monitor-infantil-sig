"""
Guía de instalación y configuración del proyecto
"""

# INSTALACIÓN - Monitor Infantil SIG

## Requisitos Previos

### Windows
1. **Python 3.11+**
   - Descargar de: https://www.python.org/downloads/
   - Durante la instalación, marcar "Add Python to PATH"

2. **PostgreSQL 15 + PostGIS 3.4**
   - Descargar de: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
   - Instalar PostGIS: https://postgis.net/windows_downloads/
   
   O usar Docker (recomendado):
   ```bash
   docker-compose up -d db
   ```

3. **Git**
   - Descargar de: https://git-scm.com/download/win

4. **OSGeo4W** (para GDAL/GEOS - GeoDjango)
   - Descargar de: https://trac.osgeo.org/osgeo4w/
   - Instalar GDAL y GEOS

## Pasos de Instalación

### 1. Clonar/Navegar al proyecto
```bash
cd C:\ProyectoSig
```

### 2. Crear entorno virtual
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements/dev.txt
```

### 4. Configurar variables de entorno
Copiar `.env.example` a `.env` y configurar:

```bash
cp .env.example .env
```

Editar `.env`:
```
SECRET_KEY=tu-secret-key-generada
DEBUG=True
DATABASE_NAME=monitor_infantil_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres123
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 5. Configurar GDAL/GEOS (Windows)
Agregar al `.env`:
```
GDAL_LIBRARY_PATH=C:\OSGeo4W\bin\gdal308.dll
GEOS_LIBRARY_PATH=C:\OSGeo4W\bin\geos_c.dll
```

### 6. Crear base de datos
```sql
-- Conectar a PostgreSQL como superusuario
CREATE DATABASE monitor_infantil_db;
\c monitor_infantil_db
CREATE EXTENSION postgis;
```

O usar Docker:
```bash
docker-compose up -d db
# La base de datos se crea automáticamente con PostGIS
```

### 7. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Crear superusuario
```bash
python manage.py createsuperuser
```

### 9. Cargar datos de prueba (opcional)
```bash
python manage.py loaddata fixtures/initial_data.json
```

### 10. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

Abrir: http://localhost:8000/admin

## Configuración de Docker (Alternativa Recomendada)

### 1. Instalar Docker Desktop
https://www.docker.com/products/docker-desktop/

### 2. Levantar servicios
```bash
docker-compose up -d
```

Esto levanta:
- PostgreSQL + PostGIS en puerto 5432
- Redis en puerto 6379

### 3. Ejecutar migraciones dentro del contenedor
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Verificar Instalación

### 1. Verificar GeoDjango
```bash
python manage.py shell
```

```python
from django.contrib.gis.geos import Point
p = Point(-63.1812, -17.7833, srid=4326)
print(p)
# Debe mostrar: SRID=4326;POINT (-63.1812 -17.7833)
```

### 2. Verificar PostGIS
```bash
python manage.py dbshell
```

```sql
SELECT PostGIS_Version();
-- Debe mostrar la versión de PostGIS
```

## Problemas Comunes

### Error: GDAL library not found
**Solución**: Instalar OSGeo4W y configurar rutas en `.env`

### Error: Could not find the GEOS library
**Solución**: Verificar instalación de GEOS en OSGeo4W

### Error: PostgreSQL connection failed
**Solución**: Verificar que PostgreSQL esté ejecutándose y las credenciales en `.env`

### Error: PostGIS extension not found
**Solución**: Ejecutar `CREATE EXTENSION postgis;` en la base de datos

## Siguiente Paso

Una vez instalado, ver:
- **Tutorial de uso**: `docs/TUTORIAL.md`
- **Documentación de API**: `apps/api/API_DOCS.md`
- **Guía de desarrollo**: `docs/DESARROLLO.md`
