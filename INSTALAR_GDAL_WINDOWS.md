# Instalar GDAL en Windows para GeoDjango

## Opción 1: OSGeo4W (Recomendado)

1. **Descargar OSGeo4W:**
   - Ve a: https://trac.osgeo.org/osgeo4w/
   - Descarga el instalador: https://download.osgeo.org/osgeo4w/v2/osgeo4w-setup.exe

2. **Instalar:**
   - Ejecuta el instalador
   - Selecciona "Express Install"
   - Marca "GDAL" y "QGIS" (opcional)
   - Instala en la ruta por defecto: `C:\OSGeo4W`

3. **Configurar Django:**
   
   Agrega estas líneas al final de `config/settings.py`:
   
   ```python
   # GDAL Windows paths (OSGeo4W)
   if os.name == 'nt':  # Windows
       OSGEO4W = r"C:\OSGeo4W"
       if os.path.isdir(OSGEO4W):
           os.environ['OSGEO4W_ROOT'] = OSGEO4W
           os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
           os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
           os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']
           GDAL_LIBRARY_PATH = OSGEO4W + r"\bin\gdal309.dll"
           GEOS_LIBRARY_PATH = OSGEO4W + r"\bin\geos_c.dll"
   ```

## Opción 2: Wheel precompilado

1. **Descargar wheel de GDAL:**
   - Ve a: https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
   - Descarga el archivo `.whl` para tu versión de Python (ej: `GDAL‑3.8.5‑cp311‑cp311‑win_amd64.whl` para Python 3.11)

2. **Instalar:**
   ```bash
   pip install GDAL‑3.8.5‑cp311‑cp311‑win_amd64.whl
   ```

## Opción 3: Usar Docker (Más fácil)

Si tienes Docker Desktop instalado:

```bash
cd c:\ProyectoSig\backend
docker-compose up
```

Esto levantará Django con todas las dependencias GIS ya configuradas.

## Verificar instalación

```python
python manage.py shell
>>> from django.contrib.gis.geos import Point
>>> p = Point(-63.1812, -17.7833)
>>> print(p)
```

Si no imprime error, GDAL está correctamente instalado.

## Alternativa: Ejecutar en el servidor

Si no quieres instalar GDAL en Windows, simplemente:

1. **Haz los cambios de código en Windows**
2. **Sube los cambios al servidor:**
   ```bash
   git add .
   git commit -m "Fix serializers"
   git push
   ```

3. **En el servidor SSH, actualiza y reinicia:**
   ```bash
   cd /opt/monitor-infantil-sig/backend
   git pull
   sudo systemctl restart gunicorn
   ```

De esta forma solo desarrollas código en Windows y ejecutas en el servidor donde ya está todo configurado.
