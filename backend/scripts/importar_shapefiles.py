"""
Script para importar shapefiles de kinders a PostgreSQL/PostGIS
Usa LayerMapping de GeoDjango para importar geometrías
"""
import os
import sys
from pathlib import Path

# Configurar Django
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.gis.utils import LayerMapping
from apps.gis_tracking.models import CentroEducativo


# Mapeo de campos del shapefile a modelo Django
centro_mapping = {
    'codigo': 'CODIGO',
    'nombre': 'NOMBRE',
    'direccion': 'DIRECCION',
    'telefono': 'TELEFONO',
    'area_segura': 'POLYGON',
}


def importar_shapefiles():
    """
    Importa shapefiles de kinders a la base de datos
    """
    print("=" * 60)
    print("📥 IMPORTANDO SHAPEFILES A POSTGRESQL")
    print("=" * 60)
    
    # Ruta del shapefile
    shapefile_path = backend_dir / 'data' / 'shapefiles' / 'kinders_santacruz.shp'
    
    if not shapefile_path.exists():
        print(f"\n❌ Error: Shapefile no encontrado")
        print(f"   📁 Esperado en: {shapefile_path}")
        print(f"\n   Ejecuta primero: python scripts/crear_shapefiles_kinders.py")
        return
    
    print(f"\n📂 Shapefile encontrado:")
    print(f"   {shapefile_path}")
    
    # Preguntar si eliminar datos existentes
    print(f"\n⚠️  Registros existentes en BD: {CentroEducativo.objects.count()}")
    
    respuesta = input("\n¿Eliminar registros existentes antes de importar? (s/N): ").strip().lower()
    
    if respuesta == 's':
        count = CentroEducativo.objects.count()
        CentroEducativo.objects.all().delete()
        print(f"   🗑️  {count} registros eliminados")
    
    # Importar usando LayerMapping
    print(f"\n📥 Importando datos...")
    
    try:
        lm = LayerMapping(
            CentroEducativo,
            str(shapefile_path),
            centro_mapping,
            transform=True,  # Transformar al SRID del modelo si es necesario
            encoding='utf-8'
        )
        
        # Guardar con verbose para ver el progreso
        lm.save(strict=True, verbose=True)
        
        print(f"\n✅ Importación completada")
        print(f"   📊 Total de kinders: {CentroEducativo.objects.count()}")
        
        # Mostrar resumen
        print(f"\n📋 Kinders importados:")
        for idx, kinder in enumerate(CentroEducativo.objects.all(), 1):
            print(f"   {idx}. {kinder.nombre}")
            print(f"      📍 {kinder.direccion}")
            print(f"      📞 {kinder.telefono}")
            print(f"      🗺️  Área: {kinder.area_segura.area:.6f} grados²")
            print()
        
    except Exception as e:
        print(f"\n❌ Error durante la importación: {e}")
        import traceback
        traceback.print_exc()


def verificar_importacion():
    """
    Verifica que los datos se importaron correctamente
    """
    print("\n" + "=" * 60)
    print("✅ VERIFICACIÓN DE IMPORTACIÓN")
    print("=" * 60)
    
    total = CentroEducativo.objects.count()
    print(f"\n📊 Total de centros educativos: {total}")
    
    if total == 0:
        print("⚠️  No hay datos importados")
        return
    
    # Verificar geometrías
    print(f"\n🗺️  Verificando geometrías:")
    for kinder in CentroEducativo.objects.all():
        if kinder.area_segura:
            centroid = kinder.area_segura.centroid
            print(f"   ✅ {kinder.codigo}: Centro en ({centroid.x:.4f}, {centroid.y:.4f})")
        else:
            print(f"   ❌ {kinder.codigo}: Sin geometría")
    
    # Verificar sistema de coordenadas
    primer_kinder = CentroEducativo.objects.first()
    if primer_kinder and primer_kinder.area_segura:
        srid = primer_kinder.area_segura.srid
        print(f"\n🌍 Sistema de coordenadas: EPSG:{srid}")
        
        if srid != 4326:
            print(f"   ⚠️  Advertencia: Se esperaba EPSG:4326 (WGS84)")


if __name__ == '__main__':
    try:
        importar_shapefiles()
        verificar_importacion()
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
        print("\n📍 Próximos pasos:")
        print("   1. Verificar en Django Admin: http://143.198.30.170:8000/admin/")
        print("   2. Probar API: http://143.198.30.170:8000/api/centros-educativos/")
        print("   3. Visualizar en app móvil")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Importación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
