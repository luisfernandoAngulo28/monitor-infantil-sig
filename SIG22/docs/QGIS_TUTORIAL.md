# 🗺️ Guía QGIS - Digitalización de Áreas de Kinders

## Objetivo
Digitalizar el polígono del área segura del Kinder usando QGIS y exportarlo para usarlo en el sistema.

---

## 📥 1. Instalación de QGIS

### Windows
1. Descargar desde: https://qgis.org/es/site/forusers/download.html
2. Instalar **QGIS Standalone Installer** (versión LTR recomendada)
3. Ejecutar QGIS Desktop

---

## 🗺️ 2. Crear Proyecto y Capa Base

### Paso 1: Crear Nuevo Proyecto
1. Abrir QGIS
2. **Proyecto → Nuevo**
3. Guardar como: `kinder_areas.qgz`

### Paso 2: Agregar Mapa Base (OpenStreetMap)
1. **Panel Navegador** (izquierda) → **XYZ Tiles**
2. Click derecho en **OpenStreetMap** → **Agregar capa al proyecto**
3. El mapa mundial aparecerá en el canvas

### Paso 3: Navegar al Área del Kinder
1. Usar **herramienta de zoom** o **búsqueda**
2. Buscar la dirección del kinder (ej: "Av. San Martin, Santa Cruz, Bolivia")
3. Hacer zoom hasta ver claramente el edificio

---

## ✏️ 3. Crear Capa Vectorial para Polígonos

### Paso 1: Nueva Capa Shapefile
1. **Capa → Crear Capa → Nueva Capa de Archivo Shape**
2. Configurar:
   - **Tipo de geometría**: Polígono
   - **SRC** (Sistema de Referencia): **EPSG:4326 - WGS 84** (GPS estándar)
   - **Nombre del archivo**: `kinder_los_pitufos.shp`
   
3. **Agregar campos** (atributos):
   - `nombre` → Texto, longitud 200
   - `codigo` → Texto, longitud 50
   - `direccion` → Texto, longitud 255
   
4. Click **OK**

### Paso 2: Comenzar Edición
1. Seleccionar la capa creada en el **Panel de Capas**
2. Click en **Conmutar edición** (ícono de lápiz)
3. Click en **Añadir entidad de polígono** (ícono de polígono)

---

## 🖊️ 4. Digitalizar el Polígono del Kinder

### Paso 1: Dibujar el Polígono
1. Hacer **zoom** al área exacta del kinder
2. **Click izquierdo** para cada vértice del polígono:
   - Esquina 1 del edificio
   - Esquina 2
   - Esquina 3
   - Esquina 4
   - (Si hay patio, incluirlo también)
3. **Click derecho** para finalizar el polígono

### Paso 2: Rellenar Atributos
Aparecerá un formulario:
- **nombre**: Kinder Los Pitufos
- **codigo**: KP001
- **direccion**: Av. San Martin #123

Click **OK**

### Paso 3: Guardar Cambios
1. Click en **Guardar cambios de capa** (ícono de diskette)
2. Click en **Conmutar edición** para salir del modo edición

---

## 📤 5. Exportar a GeoJSON (para Django)

### Opción 1: Exportar como GeoJSON
1. Click derecho en la capa → **Exportar → Guardar objetos como...**
2. Configurar:
   - **Formato**: GeoJSON
   - **Nombre de archivo**: `kinder_los_pitufos.geojson`
   - **SRC**: EPSG:4326
3. Click **OK**

### Opción 2: Exportar Coordenadas Manualmente
1. Abrir **Tabla de atributos** de la capa
2. Click en **Abrir calculadora de campo**
3. Crear campo calculado:
   - **Nombre**: `wkt_geometry`
   - **Tipo**: Texto
   - **Expresión**: `geom_to_wkt($geometry)`
4. Copiar el WKT (Well-Known Text) resultante

---

## 🐍 6. Importar a Django

### Método 1: Usando Django Shell + GeoJSON

```python
python manage.py shell
```

```python
import json
from django.contrib.gis.geos import GEOSGeometry
from apps.gis_tracking.models import CentroEducativo

# Leer GeoJSON
with open('kinder_los_pitufos.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Obtener geometría del primer feature
feature = data['features'][0]
geometry = feature['geometry']
properties = feature['properties']

# Crear polígono
poligono = GEOSGeometry(json.dumps(geometry))

# Crear centro educativo
kinder = CentroEducativo.objects.create(
    nombre=properties['nombre'],
    codigo=properties['codigo'],
    direccion=properties['direccion'],
    area_segura=poligono
)

print(f"✅ Centro educativo creado: {kinder}")
```

### Método 2: Usando Django Admin (Más Fácil)

1. Ir a http://localhost:8000/admin/
2. **GIS Tracking → Centros Educativos → Agregar**
3. Completar datos: nombre, código, dirección
4. En el **mapa interactivo**:
   - Usar herramienta de dibujo de polígono
   - Dibujar directamente sobre el mapa
5. Guardar

### Método 3: Copiar WKT directamente

```python
python manage.py shell
```

```python
from django.contrib.gis.geos import fromstr
from apps.gis_tracking.models import CentroEducativo

# WKT copiado desde QGIS
wkt = "POLYGON((-63.1820 -17.7840, -63.1810 -17.7840, -63.1810 -17.7830, -63.1820 -17.7830, -63.1820 -17.7840))"

poligono = fromstr(wkt, srid=4326)

kinder = CentroEducativo.objects.create(
    nombre="Kinder Los Pitufos",
    codigo="KP001",
    direccion="Av. San Martin #123",
    area_segura=poligono
)
```

---

## 🖼️ 7. Generar Mapas para el Informe

### Crear Layout de Impresión

1. **Proyecto → Nuevo diseño de impresión**
2. Nombre: "Mapa Área Kinder"
3. **Agregar → Agregar Mapa**
4. Dibujar rectángulo en el canvas
5. **Agregar elementos**:
   - Título: "Área Segura - Kinder Los Pitufos"
   - Escala gráfica
   - Flecha de Norte
   - Leyenda
   - Etiquetas

### Exportar como Imagen

1. **Diseño → Exportar como imagen**
2. Formato: PNG (300 dpi)
3. Guardar como: `mapa_kinder_area.png`

### Exportar como PDF

1. **Diseño → Exportar como PDF**
2. Guardar como: `mapa_kinder_area.pdf`

---

## 📊 8. Análisis Espacial en QGIS (Opcional)

### Calcular Área del Polígono

1. Abrir **Tabla de atributos**
2. **Abrir calculadora de campo**
3. Crear campo:
   - Nombre: `area_m2`
   - Tipo: Número decimal
   - Expresión: `$area` (área en metros cuadrados)

### Crear Buffer (Margen de Seguridad)

1. **Vector → Herramientas de geoproceso → Buffer**
2. Configurar:
   - **Capa de entrada**: kinder_los_pitufos
   - **Distancia**: 50 (metros)
   - **Segmentos**: 20
3. Resultado: polígono expandido 50m en todas direcciones

---

## 🔍 9. Validación del Polígono

### Verificar Topología
1. **Vector → Herramientas de topología → Comprobar validez de geometrías**
2. Revisar si hay:
   - Polígonos autointersectantes
   - Huecos no deseados
   - Vértices duplicados

### Simplificar Geometría (si es complejo)
1. **Vector → Herramientas de geometría → Simplificar**
2. Tolerancia: 0.0001

---

## 📝 10. Documentación para el Informe

### Capturas de Pantalla Necesarias

1. **Vista general del área**
   - Mapa con OpenStreetMap de fondo
   - Polígono digitalizado visible

2. **Mapa con layout profesional**
   - Título, escala, norte, leyenda
   - Exportado como PNG/PDF

3. **Tabla de atributos**
   - Mostrando campos: nombre, código, área

### Metadatos a Incluir en el Informe

```
Centro Educativo: Kinder Los Pitufos
Código: KP001
Sistema de Coordenadas: EPSG:4326 (WGS 84)
Área: XXX m²
Perímetro: XXX m
Fecha de digitalización: 22/11/2025
Software utilizado: QGIS 3.34
Fuente cartográfica: OpenStreetMap
```

---

## 🎓 Ejemplo para Múltiples Kinders

Si necesitas digitalizar varios kinders:

1. Usar la **misma capa** (kinder_areas.shp)
2. Agregar múltiples polígonos (uno por kinder)
3. Cada uno con sus atributos propios
4. Exportar todo el shapefile
5. Importar masivamente a Django:

```python
from django.contrib.gis.utils import LayerMapping
from apps.gis_tracking.models import CentroEducativo

mapping = {
    'nombre': 'nombre',
    'codigo': 'codigo',
    'direccion': 'direccion',
    'area_segura': 'POLYGON',
}

lm = LayerMapping(CentroEducativo, 'kinder_areas.shp', mapping)
lm.save(verbose=True)
```

---

## ✅ Checklist Final

- [ ] QGIS instalado
- [ ] Capa vectorial creada (EPSG:4326)
- [ ] Polígono del kinder digitalizado
- [ ] Atributos completados (nombre, código, dirección)
- [ ] GeoJSON exportado
- [ ] Importado a Django
- [ ] Verificado en Django Admin (aparece en el mapa)
- [ ] Mapa generado para informe (con layout)
- [ ] Captura de pantalla guardada

---

¡Listo para digitalizar! 🗺️
