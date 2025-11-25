"""
Script para configurar la base de datos GeoDjango con datos de ejemplo
Ejecutar: python setup_gis_db.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.gis.geos import Point, Polygon
from apps.core.models import Usuario, Tutor
from apps.gis_tracking.models import CentroEducativo, Nino, PosicionGPS
from datetime import date, datetime
from django.utils import timezone


def crear_centros_educativos():
    """
    Crear centros educativos de ejemplo en Santa Cruz de la Sierra
    con polígonos que representan el área del kinder
    """
    print("📍 Creando centros educativos...")
    
    # Centro 1: Kinder en zona Norte de Santa Cruz
    # Coordenadas aproximadas de un kinder real
    # Polígono pequeño que representa el terreno del kinder (aprox 50x50 metros)
    coords_kinder1 = [
        (-17.7748, -63.1812),  # Esquina NO
        (-17.7748, -63.1808),  # Esquina NE
        (-17.7752, -63.1808),  # Esquina SE
        (-17.7752, -63.1812),  # Esquina SO
        (-17.7748, -63.1812),  # Cerrar polígono
    ]
    
    centro1, created = CentroEducativo.objects.get_or_create(
        codigo='KINDER-001',
        defaults={
            'nombre': 'Jardín Infantil Los Pitufos',
            'direccion': 'Av. San Martín entre 3er y 4to anillo',
            'telefono': '3-3334455',
            'email': 'contacto@lospitufos.edu.bo',
            'area_segura': Polygon(coords_kinder1),
            'margen_metros': 20,  # 20 metros de margen
            'activo': True
        }
    )
    if created:
        print(f"  ✅ {centro1.nombre}")
    
    # Centro 2: Kinder en zona Centro
    coords_kinder2 = [
        (-17.7838, -63.1822),
        (-17.7838, -63.1818),
        (-17.7842, -63.1818),
        (-17.7842, -63.1822),
        (-17.7838, -63.1822),
    ]
    
    centro2, created = CentroEducativo.objects.get_or_create(
        codigo='KINDER-002',
        defaults={
            'nombre': 'Centro Educativo Rayito de Sol',
            'direccion': 'Calle Sucre esquina Junín',
            'telefono': '3-3556677',
            'email': 'info@rayitodesol.edu.bo',
            'area_segura': Polygon(coords_kinder2),
            'margen_metros': 15,
            'activo': True
        }
    )
    if created:
        print(f"  ✅ {centro2.nombre}")
    
    return centro1, centro2


def crear_usuarios_tutores():
    """
    Crear usuarios y tutores de ejemplo
    """
    print("\n👤 Creando usuarios y tutores...")
    
    # Tutor 1
    user1, created = Usuario.objects.get_or_create(
        username='maria.lopez',
        defaults={
            'email': 'maria.lopez@gmail.com',
            'first_name': 'María',
            'last_name': 'López González',
            'tipo_usuario': 'TUTOR'
        }
    )
    if created:
        user1.set_password('demo123456')
        user1.save()
        print(f"  ✅ Usuario: {user1.username}")
    
    tutor1, created = Tutor.objects.get_or_create(
        usuario=user1,
        defaults={
            'ci': '1234567 SC',
            'relacion': 'MADRE',
            'telefono_emergencia': '70123456'
        }
    )
    if created:
        print(f"  ✅ Tutor: {tutor1}")
    
    # Tutor 2
    user2, created = Usuario.objects.get_or_create(
        username='juan.perez',
        defaults={
            'email': 'juan.perez@gmail.com',
            'first_name': 'Juan',
            'last_name': 'Pérez Rojas',
            'tipo_usuario': 'TUTOR'
        }
    )
    if created:
        user2.set_password('demo123456')
        user2.save()
        print(f"  ✅ Usuario: {user2.username}")
    
    tutor2, created = Tutor.objects.get_or_create(
        usuario=user2,
        defaults={
            'ci': '7654321 SC',
            'relacion': 'PADRE',
            'telefono_emergencia': '75987654'
        }
    )
    if created:
        print(f"  ✅ Tutor: {tutor2}")
    
    return tutor1, tutor2


def crear_ninos(centro1, centro2, tutor1, tutor2):
    """
    Crear niños de ejemplo asignados a los kinders
    """
    print("\n👶 Creando niños...")
    
    nino1, created = Nino.objects.get_or_create(
        nombre='Sofía',
        apellido_paterno='López',
        apellido_materno='Ramírez',
        defaults={
            'fecha_nacimiento': date(2020, 5, 15),
            'sexo': 'F',
            'centro_educativo': centro1,
            'tutor_principal': tutor1,
            'tracking_activo': True,
            'activo': True
        }
    )
    if created:
        print(f"  ✅ {nino1.nombre_completo()} - {nino1.edad} años")
    
    nino2, created = Nino.objects.get_or_create(
        nombre='Mateo',
        apellido_paterno='Pérez',
        apellido_materno='García',
        defaults={
            'fecha_nacimiento': date(2019, 8, 22),
            'sexo': 'M',
            'centro_educativo': centro1,
            'tutor_principal': tutor2,
            'tracking_activo': True,
            'activo': True
        }
    )
    if created:
        print(f"  ✅ {nino2.nombre_completo()} - {nino2.edad} años")
    
    nino3, created = Nino.objects.get_or_create(
        nombre='Valentina',
        apellido_paterno='González',
        apellido_materno='Silva',
        defaults={
            'fecha_nacimiento': date(2021, 3, 10),
            'sexo': 'F',
            'centro_educativo': centro2,
            'tutor_principal': tutor1,
            'tracking_activo': True,
            'activo': True
        }
    )
    if created:
        print(f"  ✅ {nino3.nombre_completo()} - {nino3.edad} años")
    
    return nino1, nino2, nino3


def crear_posiciones_ejemplo(nino1, nino2, nino3):
    """
    Crear posiciones GPS de ejemplo
    - Algunas dentro del área segura
    - Algunas fuera (para generar alertas)
    """
    print("\n📡 Creando posiciones GPS de ejemplo...")
    
    # Posiciones DENTRO del área del Kinder 1 (Sofía y Mateo)
    PosicionGPS.objects.create(
        nino=nino1,
        ubicacion=Point(-63.1810, -17.7750, srid=4326),  # Dentro
        precision_metros=5.0,
        nivel_bateria=85,
        timestamp=timezone.now()
    )
    print(f"  ✅ {nino1.nombre} - Posición SEGURA (dentro del kinder)")
    
    PosicionGPS.objects.create(
        nino=nino2,
        ubicacion=Point(-63.1809, -17.7750, srid=4326),  # Dentro
        precision_metros=8.0,
        nivel_bateria=92,
        timestamp=timezone.now()
    )
    print(f"  ✅ {nino2.nombre} - Posición SEGURA (dentro del kinder)")
    
    # Posición FUERA del área (generará alerta)
    PosicionGPS.objects.create(
        nino=nino3,
        ubicacion=Point(-63.1850, -17.7850, srid=4326),  # Lejos del kinder
        precision_metros=10.0,
        nivel_bateria=65,
        timestamp=timezone.now()
    )
    print(f"  ⚠️  {nino3.nombre} - Posición FUERA del área (ALERTA generada)")


def main():
    print("=" * 60)
    print("🚀 CONFIGURACIÓN DE BASE DE DATOS GEODJANGO")
    print("=" * 60)
    
    try:
        # 1. Crear centros educativos con polígonos
        centro1, centro2 = crear_centros_educativos()
        
        # 2. Crear usuarios y tutores
        tutor1, tutor2 = crear_usuarios_tutores()
        
        # 3. Crear niños
        nino1, nino2, nino3 = crear_ninos(centro1, centro2, tutor1, tutor2)
        
        # 4. Crear posiciones GPS de ejemplo
        crear_posiciones_ejemplo(nino1, nino2, nino3)
        
        print("\n" + "=" * 60)
        print("✅ BASE DE DATOS CONFIGURADA EXITOSAMENTE")
        print("=" * 60)
        print("\n📋 RESUMEN:")
        print(f"  • Centros educativos: {CentroEducativo.objects.count()}")
        print(f"  • Tutores: {Tutor.objects.count()}")
        print(f"  • Niños: {Nino.objects.count()}")
        print(f"  • Posiciones GPS: {PosicionGPS.objects.count()}")
        
        print("\n🔑 CREDENCIALES DE PRUEBA:")
        print("  Usuario 1: maria.lopez / demo123456")
        print("  Usuario 2: juan.perez / demo123456")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
