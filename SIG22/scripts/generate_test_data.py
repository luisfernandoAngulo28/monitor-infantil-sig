"""
Script para generar datos de prueba para el sistema Monitor Infantil SIG
"""
import os
import sys
import django
from datetime import date, timedelta
from django.utils import timezone

# Configurar Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.gis.geos import Point, Polygon
from apps.core.models import Usuario, Tutor
from apps.gis_tracking.models import CentroEducativo, Nino, PosicionGPS


def crear_centro_educativo():
    """Crea un centro educativo de prueba"""
    print("📍 Creando Centro Educativo de prueba...")
    
    # Polígono del Kinder (área aproximada en Santa Cruz)
    poligono = Polygon((
        (-63.1820, -17.7840),
        (-63.1810, -17.7840),
        (-63.1810, -17.7830),
        (-63.1820, -17.7830),
        (-63.1820, -17.7840),
    ), srid=4326)
    
    kinder, created = CentroEducativo.objects.get_or_create(
        codigo='KP001',
        defaults={
            'nombre': 'Kinder Los Pitufos',
            'direccion': 'Av. San Martin #123, Santa Cruz',
            'telefono': '3-3456789',
            'area_segura': poligono,
        }
    )
    
    if created:
        print(f"✅ Centro educativo creado: {kinder.nombre}")
    else:
        print(f"ℹ️ Centro educativo ya existe: {kinder.nombre}")
    
    return kinder


def crear_tutores():
    """Crea tutores de prueba"""
    print("\n👥 Creando Tutores de prueba...")
    
    tutores_data = [
        {
            'username': 'maria_gonzalez',
            'email': 'maria@example.com',
            'first_name': 'María',
            'last_name': 'González',
            'ci': '12345678',
            'relacion': 'MADRE',
        },
        {
            'username': 'jose_perez',
            'email': 'jose@example.com',
            'first_name': 'José',
            'last_name': 'Pérez',
            'ci': '87654321',
            'relacion': 'PADRE',
        },
    ]
    
    tutores = []
    for data in tutores_data:
        usuario, created = Usuario.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'tipo_usuario': 'TUTOR',
            }
        )
        
        if created:
            usuario.set_password('test123')
            usuario.save()
            print(f"✅ Usuario creado: {usuario.username}")
        
        tutor, created = Tutor.objects.get_or_create(
            usuario=usuario,
            defaults={
                'ci': data['ci'],
                'relacion': data['relacion'],
                'telefono_emergencia': '70123456',
            }
        )
        
        if created:
            print(f"✅ Tutor creado: {tutor}")
        
        tutores.append(tutor)
    
    return tutores


def crear_ninos(kinder, tutores):
    """Crea niños de prueba"""
    print("\n👶 Creando Niños de prueba...")
    
    ninos_data = [
        {
            'nombre': 'Pedrito',
            'apellido_paterno': 'González',
            'apellido_materno': 'López',
            'fecha_nacimiento': date(2020, 5, 15),
            'sexo': 'M',
            'tutor': tutores[0],
        },
        {
            'nombre': 'Anita',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'Martínez',
            'fecha_nacimiento': date(2021, 3, 20),
            'sexo': 'F',
            'tutor': tutores[1],
        },
    ]
    
    ninos = []
    for i, data in enumerate(ninos_data):
        nino, created = Nino.objects.get_or_create(
            nombre=data['nombre'],
            apellido_paterno=data['apellido_paterno'],
            defaults={
                'apellido_materno': data['apellido_materno'],
                'fecha_nacimiento': data['fecha_nacimiento'],
                'sexo': data['sexo'],
                'centro_educativo': kinder,
                'tutor_principal': data['tutor'],
                'dispositivo_id': f'device_00{i+1}',
                'tracking_activo': True,
            }
        )
        
        if created:
            print(f"✅ Niño creado: {nino.nombre_completo()}")
        else:
            print(f"ℹ️ Niño ya existe: {nino.nombre_completo()}")
        
        ninos.append(nino)
    
    return ninos


def crear_posiciones_gps(ninos):
    """Crea posiciones GPS de prueba"""
    print("\n📍 Creando Posiciones GPS de prueba...")
    
    # Posiciones dentro del área
    posiciones_dentro = [
        (-63.1815, -17.7835),  # Centro del área
        (-63.1816, -17.7836),
        (-63.1814, -17.7834),
    ]
    
    # Posiciones fuera del área
    posiciones_fuera = [
        (-63.1900, -17.7900),  # Lejos del área
    ]
    
    for nino in ninos:
        # Crear posiciones dentro
        for lng, lat in posiciones_dentro:
            punto = Point(lng, lat, srid=4326)
            pos = PosicionGPS.objects.create(
                nino=nino,
                ubicacion=punto,
                precision_metros=10.5,
                nivel_bateria=85,
            )
            print(f"✅ Posición GPS creada (dentro): {nino.nombre} - {pos.timestamp}")
        
        # Crear una posición fuera (genera alerta)
        lng, lat = posiciones_fuera[0]
        punto = Point(lng, lat, srid=4326)
        pos = PosicionGPS.objects.create(
            nino=nino,
            ubicacion=punto,
            precision_metros=8.0,
            nivel_bateria=80,
        )
        print(f"⚠️ Posición GPS creada (FUERA): {nino.nombre} - {pos.timestamp}")


def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 Generando Datos de Prueba - Monitor Infantil SIG")
    print("=" * 60)
    
    try:
        kinder = crear_centro_educativo()
        tutores = crear_tutores()
        ninos = crear_ninos(kinder, tutores)
        crear_posiciones_gps(ninos)
        
        print("\n" + "=" * 60)
        print("✅ ¡Datos de prueba generados exitosamente!")
        print("=" * 60)
        print("\n📊 Resumen:")
        print(f"   - Centros educativos: {CentroEducativo.objects.count()}")
        print(f"   - Tutores: {Tutor.objects.count()}")
        print(f"   - Niños: {Nino.objects.count()}")
        print(f"   - Posiciones GPS: {PosicionGPS.objects.count()}")
        
        print("\n🔐 Credenciales de prueba:")
        print("   Usuario: maria_gonzalez")
        print("   Password: test123")
        print("\n   Usuario: jose_perez")
        print("   Password: test123")
        
        print("\n🌐 URLs:")
        print("   - Admin: http://localhost:8000/admin/")
        print("   - API: http://localhost:8000/api/")
        print("   - Dashboard: http://localhost:8000/")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
