"""
Script para crear shapefiles de ejemplo de Kinders en Santa Cruz de la Sierra
Genera archivos .shp con polígonos de áreas de centros educativos
"""
import os
import sys
from pathlib import Path

# Añadir el directorio backend al path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    import django
    django.setup()
except Exception as e:
    print(f"⚠️  Ejecutando sin Django: {e}")

try:
    from osgeo import ogr, osr
    import json
except ImportError:
    print("❌ Error: Necesitas instalar GDAL")
    print("Ejecuta: pip install GDAL")
    sys.exit(1)


def crear_shapefile_kinders():
    """
    Crea un shapefile con polígonos de kinders de Santa Cruz
    """
    print("=" * 60)
    print("🗺️  CREANDO SHAPEFILE DE KINDERS - SANTA CRUZ")
    print("=" * 60)
    
    # Directorio de salida
    output_dir = backend_dir / 'data' / 'shapefiles'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    shapefile_path = output_dir / 'kinders_santacruz.shp'
    
    # Eliminar shapefile existente
    driver = ogr.GetDriverByName('ESRI Shapefile')
    if shapefile_path.exists():
        driver.DeleteDataSource(str(shapefile_path))
    
    # Crear nuevo shapefile
    ds = driver.CreateDataSource(str(shapefile_path))
    
    # Sistema de coordenadas WGS84 (EPSG:4326)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    
    # Crear capa de polígonos
    layer = ds.CreateLayer('kinders', srs, ogr.wkbPolygon)
    
    # Definir campos (atributos)
    layer.CreateField(ogr.FieldDefn('CODIGO', ogr.OFTString))
    layer.CreateField(ogr.FieldDefn('NOMBRE', ogr.OFTString))
    layer.CreateField(ogr.FieldDefn('DIRECCION', ogr.OFTString))
    layer.CreateField(ogr.FieldDefn('TELEFONO', ogr.OFTString))
    layer.CreateField(ogr.FieldDefn('ZONA', ogr.OFTString))
    
    # Datos de kinders de ejemplo en Santa Cruz
    kinders = [
        {
            'codigo': 'K-SCZ-001',
            'nombre': 'Kinder Pequeños Exploradores',
            'direccion': 'Av. Roca y Coronado, Zona Norte',
            'telefono': '3-3334455',
            'zona': 'Norte',
            # Polígono pequeño en zona norte de Santa Cruz
            'coords': [
                (-63.1820, -17.7740),
                (-63.1810, -17.7740),
                (-63.1810, -17.7750),
                (-63.1820, -17.7750),
                (-63.1820, -17.7740),
            ]
        },
        {
            'codigo': 'K-SCZ-002',
            'nombre': 'Centro Educativo Rayito de Sol',
            'direccion': 'Calle Sucre esquina Junín, Zona Centro',
            'telefono': '3-3556677',
            'zona': 'Centro',
            # Polígono en zona centro
            'coords': [
                (-63.1830, -17.7800),
                (-63.1818, -17.7800),
                (-63.1818, -17.7812),
                (-63.1830, -17.7812),
                (-63.1830, -17.7800),
            ]
        },
        {
            'codigo': 'K-SCZ-003',
            'nombre': 'Jardín Infantil Las Palmeras',
            'direccion': '4to Anillo entre Beni y Piraí',
            'telefono': '3-3778899',
            'zona': 'Este',
            # Polígono zona este
            'coords': [
                (-63.1700, -17.7850),
                (-63.1688, -17.7850),
                (-63.1688, -17.7865),
                (-63.1700, -17.7865),
                (-63.1700, -17.7850),
            ]
        },
        {
            'codigo': 'K-SCZ-004',
            'nombre': 'Kinder Mi Primer Pasito',
            'direccion': 'Av. Santos Dumont, Equipetrol',
            'telefono': '3-3991122',
            'zona': 'Norte',
            # Polígono en Equipetrol
            'coords': [
                (-63.1650, -17.7700),
                (-63.1638, -17.7700),
                (-63.1638, -17.7715),
                (-63.1650, -17.7715),
                (-63.1650, -17.7700),
            ]
        },
        {
            'codigo': 'K-SCZ-005',
            'nombre': 'Centro Infantil Arcoíris',
            'direccion': 'Plan 3000, Manzana 15',
            'telefono': '3-3223344',
            'zona': 'Plan 3000',
            # Polígono en Plan 3000
            'coords': [
                (-63.1200, -17.7400),
                (-63.1188, -17.7400),
                (-63.1188, -17.7415),
                (-63.1200, -17.7415),
                (-63.1200, -17.7400),
            ]
        },
    ]
    
    print(f"\n📝 Creando {len(kinders)} kinders...\n")
    
    # Crear features (registros)
    for idx, kinder in enumerate(kinders, 1):
        # Crear polígono
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for lon, lat in kinder['coords']:
            ring.AddPoint(lon, lat)
        
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        
        # Crear feature
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetGeometry(poly)
        feature.SetField('CODIGO', kinder['codigo'])
        feature.SetField('NOMBRE', kinder['nombre'])
        feature.SetField('DIRECCION', kinder['direccion'])
        feature.SetField('TELEFONO', kinder['telefono'])
        feature.SetField('ZONA', kinder['zona'])
        
        layer.CreateFeature(feature)
        feature = None
        
        print(f"  ✅ {idx}. {kinder['nombre']} ({kinder['zona']})")
    
    # Cerrar datasource
    ds = None
    
    print(f"\n✅ Shapefile creado exitosamente:")
    print(f"   📁 {shapefile_path}")
    print(f"   📊 {len(kinders)} registros")
    
    # Listar archivos generados
    print(f"\n📦 Archivos generados:")
    for ext in ['.shp', '.shx', '.dbf', '.prj']:
        file_path = shapefile_path.with_suffix(ext)
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"   • {file_path.name} ({size_kb:.1f} KB)")
    
    return shapefile_path


def crear_geojson_kinders():
    """
    Crea también un archivo GeoJSON para visualización web
    """
    print("\n" + "=" * 60)
    print("🌐 CREANDO GEOJSON DE KINDERS")
    print("=" * 60)
    
    output_dir = backend_dir / 'data' / 'shapefiles'
    geojson_path = output_dir / 'kinders_santacruz.geojson'
    
    kinders = [
        {
            'codigo': 'K-SCZ-001',
            'nombre': 'Kinder Pequeños Exploradores',
            'direccion': 'Av. Roca y Coronado, Zona Norte',
            'telefono': '3-3334455',
            'zona': 'Norte',
            'coords': [[
                [-63.1820, -17.7740],
                [-63.1810, -17.7740],
                [-63.1810, -17.7750],
                [-63.1820, -17.7750],
                [-63.1820, -17.7740],
            ]]
        },
        {
            'codigo': 'K-SCZ-002',
            'nombre': 'Centro Educativo Rayito de Sol',
            'direccion': 'Calle Sucre esquina Junín, Zona Centro',
            'telefono': '3-3556677',
            'zona': 'Centro',
            'coords': [[
                [-63.1830, -17.7800],
                [-63.1818, -17.7800],
                [-63.1818, -17.7812],
                [-63.1830, -17.7812],
                [-63.1830, -17.7800],
            ]]
        },
        {
            'codigo': 'K-SCZ-003',
            'nombre': 'Jardín Infantil Las Palmeras',
            'direccion': '4to Anillo entre Beni y Piraí',
            'telefono': '3-3778899',
            'zona': 'Este',
            'coords': [[
                [-63.1700, -17.7850],
                [-63.1688, -17.7850],
                [-63.1688, -17.7865],
                [-63.1700, -17.7865],
                [-63.1700, -17.7850],
            ]]
        },
        {
            'codigo': 'K-SCZ-004',
            'nombre': 'Kinder Mi Primer Pasito',
            'direccion': 'Av. Santos Dumont, Equipetrol',
            'telefono': '3-3991122',
            'zona': 'Norte',
            'coords': [[
                [-63.1650, -17.7700],
                [-63.1638, -17.7700],
                [-63.1638, -17.7715],
                [-63.1650, -17.7715],
                [-63.1650, -17.7700],
            ]]
        },
        {
            'codigo': 'K-SCZ-005',
            'nombre': 'Centro Infantil Arcoíris',
            'direccion': 'Plan 3000, Manzana 15',
            'telefono': '3-3223344',
            'zona': 'Plan 3000',
            'coords': [[
                [-63.1200, -17.7400],
                [-63.1188, -17.7400],
                [-63.1188, -17.7415],
                [-63.1200, -17.7415],
                [-63.1200, -17.7400],
            ]]
        },
    ]
    
    geojson = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "EPSG:4326"
            }
        },
        "features": []
    }
    
    for kinder in kinders:
        feature = {
            "type": "Feature",
            "properties": {
                "codigo": kinder['codigo'],
                "nombre": kinder['nombre'],
                "direccion": kinder['direccion'],
                "telefono": kinder['telefono'],
                "zona": kinder['zona']
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": kinder['coords']
            }
        }
        geojson['features'].append(feature)
    
    with open(geojson_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ GeoJSON creado:")
    print(f"   📁 {geojson_path}")
    print(f"   📊 {len(kinders)} features")
    
    return geojson_path


if __name__ == '__main__':
    try:
        # Crear shapefile
        shp_path = crear_shapefile_kinders()
        
        # Crear GeoJSON
        geojson_path = crear_geojson_kinders()
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
        print("\n📍 Próximos pasos:")
        print("   1. Ejecutar script de importación a PostgreSQL")
        print("   2. Verificar datos en Django Admin")
        print("   3. Visualizar en la app móvil")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
