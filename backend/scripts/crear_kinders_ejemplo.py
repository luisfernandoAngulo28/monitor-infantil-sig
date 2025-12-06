"""
Script para crear kinders de ejemplo directamente en PostgreSQL
Sin necesidad de GDAL o shapefiles
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

from django.contrib.gis.geos import Polygon
from apps.gis_tracking.models import CentroEducativo


def crear_kinders_santa_cruz():
    """
    Crea 5 kinders de ejemplo en Santa Cruz directamente en la BD
    """
    print("=" * 60)
    print("🏫 CREANDO KINDERS DE SANTA CRUZ")
    print("=" * 60)
    
    # Datos de kinders con coordenadas reales de Santa Cruz
    kinders_data = [
        {
            'codigo': 'K-SCZ-001',
            'nombre': 'Kinder Pequeños Exploradores',
            'direccion': 'Av. Roca y Coronado, Zona Norte',
            'telefono': '3-3334455',
            'email': 'info@pequenosexploradores.edu.bo',
            # Polígono en zona norte (pequeño rectángulo)
            'coords': [
                (-63.1820, -17.7740),
                (-63.1810, -17.7740),
                (-63.1810, -17.7750),
                (-63.1820, -17.7750),
                (-63.1820, -17.7740),
            ],
            'margen_metros': 15,
        },
        {
            'codigo': 'K-SCZ-002',
            'nombre': 'Centro Educativo Rayito de Sol',
            'direccion': 'Calle Sucre esquina Junín, Zona Centro',
            'telefono': '3-3556677',
            'email': 'contacto@rayitodesol.edu.bo',
            # Polígono zona centro
            'coords': [
                (-63.1830, -17.7800),
                (-63.1818, -17.7800),
                (-63.1818, -17.7812),
                (-63.1830, -17.7812),
                (-63.1830, -17.7800),
            ],
            'margen_metros': 20,
        },
        {
            'codigo': 'K-SCZ-003',
            'nombre': 'Jardín Infantil Las Palmeras',
            'direccion': '4to Anillo entre Beni y Piraí',
            'telefono': '3-3778899',
            'email': 'administracion@laspalmeras.edu.bo',
            # Polígono zona este
            'coords': [
                (-63.1700, -17.7850),
                (-63.1688, -17.7850),
                (-63.1688, -17.7865),
                (-63.1700, -17.7865),
                (-63.1700, -17.7850),
            ],
            'margen_metros': 10,
        },
        {
            'codigo': 'K-SCZ-004',
            'nombre': 'Kinder Mi Primer Pasito',
            'direccion': 'Av. Santos Dumont, Equipetrol',
            'telefono': '3-3991122',
            'email': 'direccion@miprimerpasito.edu.bo',
            # Polígono en Equipetrol (zona residencial)
            'coords': [
                (-63.1650, -17.7700),
                (-63.1638, -17.7700),
                (-63.1638, -17.7715),
                (-63.1650, -17.7715),
                (-63.1650, -17.7700),
            ],
            'margen_metros': 25,
        },
        {
            'codigo': 'K-SCZ-005',
            'nombre': 'Centro Infantil Arcoíris',
            'direccion': 'Plan 3000, Manzana 15',
            'telefono': '3-3223344',
            'email': 'arcoiris@plan3000.edu.bo',
            # Polígono en Plan 3000
            'coords': [
                (-63.1200, -17.7400),
                (-63.1188, -17.7400),
                (-63.1188, -17.7415),
                (-63.1200, -17.7415),
                (-63.1200, -17.7400),
            ],
            'margen_metros': 30,
        },
    ]
    
    # Preguntar si eliminar datos existentes
    total_existente = CentroEducativo.objects.count()
    print(f"\n📊 Kinders existentes en BD: {total_existente}")
    
    if total_existente > 0:
        respuesta = input("\n¿Eliminar kinders existentes? (s/N): ").strip().lower()
        if respuesta == 's':
            CentroEducativo.objects.all().delete()
            print(f"   🗑️  {total_existente} kinders eliminados")
    
    # Crear kinders
    print(f"\n📝 Creando {len(kinders_data)} kinders...\n")
    
    kinders_creados = []
    
    for idx, data in enumerate(kinders_data, 1):
        # Crear polígono
        poligono = Polygon(data['coords'], srid=4326)
        
        # Crear o actualizar kinder
        kinder, created = CentroEducativo.objects.update_or_create(
            codigo=data['codigo'],
            defaults={
                'nombre': data['nombre'],
                'direccion': data['direccion'],
                'telefono': data['telefono'],
                'email': data['email'],
                'area_segura': poligono,
                'margen_metros': data['margen_metros'],
                'activo': True,
            }
        )
        
        accion = "Creado" if created else "Actualizado"
        print(f"  {'✅' if created else '🔄'} {idx}. {kinder.nombre}")
        print(f"      📍 {kinder.direccion}")
        print(f"      📞 {kinder.telefono}")
        print(f"      🗺️  Área: {poligono.area:.8f} grados² ({accion})")
        
        if kinder.ubicacion_centro:
            print(f"      🎯 Centro: ({kinder.ubicacion_centro.x:.4f}, {kinder.ubicacion_centro.y:.4f})")
        
        print()
        
        kinders_creados.append(kinder)
    
    return kinders_creados


def verificar_kinders():
    """
    Verifica los kinders creados
    """
    print("=" * 60)
    print("✅ VERIFICACIÓN")
    print("=" * 60)
    
    total = CentroEducativo.objects.count()
    print(f"\n📊 Total de kinders en BD: {total}")
    
    if total == 0:
        print("⚠️  No hay kinders en la base de datos")
        return
    
    # Listar todos
    print(f"\n📋 Lista de kinders:")
    for idx, kinder in enumerate(CentroEducativo.objects.all().order_by('codigo'), 1):
        print(f"\n{idx}. {kinder.nombre} ({kinder.codigo})")
        print(f"   📍 {kinder.direccion}")
        print(f"   📞 {kinder.telefono}")
        print(f"   ✉️  {kinder.email}")
        print(f"   🗺️  SRID: {kinder.area_segura.srid}")
        print(f"   📏 Margen: {kinder.margen_metros}m")
        print(f"   {'✅' if kinder.activo else '❌'} {'Activo' if kinder.activo else 'Inactivo'}")
        
        if kinder.ubicacion_centro:
            print(f"   🎯 Centro: Lat {kinder.ubicacion_centro.y:.4f}, Lon {kinder.ubicacion_centro.x:.4f}")


def mostrar_instrucciones():
    """
    Muestra las instrucciones para los próximos pasos
    """
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    
    print("\n📍 Próximos pasos:")
    print("\n1️⃣  Verificar en Django Admin:")
    print("    http://localhost:8000/admin/gis_tracking/centroeducativo/")
    
    print("\n2️⃣  Verificar en API REST:")
    print("    http://localhost:8000/api/centros-educativos/")
    
    print("\n3️⃣  Crear niños asociados a estos kinders:")
    print("    python manage.py shell")
    print("    >>> from apps.gis_tracking.models import CentroEducativo, Nino")
    print("    >>> kinder = CentroEducativo.objects.first()")
    
    print("\n4️⃣  Subir cambios al servidor:")
    print("    git add .")
    print("    git commit -m 'Add 5 kinders de Santa Cruz'")
    print("    git push")
    
    print("\n5️⃣  En el servidor, ejecutar:")
    print("    cd /opt/monitor-infantil-sig/backend")
    print("    source venv/bin/activate")
    print("    python scripts/crear_kinders_ejemplo.py")


if __name__ == '__main__':
    try:
        # Crear kinders
        kinders = crear_kinders_santa_cruz()
        
        # Verificar
        verificar_kinders()
        
        # Instrucciones
        mostrar_instrucciones()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
