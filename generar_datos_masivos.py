#!/usr/bin/env python3
"""
Script para crear datos masivos de prueba
Genera múltiples kinders, niños, tutores y posiciones GPS
"""

import random
from datetime import datetime, timedelta

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Cantidad de datos a generar
CANTIDAD_KINDERS = 20
CANTIDAD_NINOS = 50
POSICIONES_POR_NINO = 10  # Historial de posiciones

# Ubicaciones base en Santa Cruz, Bolivia
ZONAS_SANTA_CRUZ = [
    {"nombre": "Centro", "lat": -17.7833, "lng": -63.1821},
    {"nombre": "Plan 3000", "lat": -17.7500, "lng": -63.1500},
    {"nombre": "Equipetrol", "lat": -17.7800, "lng": -63.1700},
    {"nombre": "Urbarí", "lat": -17.7600, "lng": -63.1600},
    {"nombre": "Pampa de la Isla", "lat": -17.8000, "lng": -63.1900},
]

# Nombres para kinders (20)
NOMBRES_KINDERS = [
    "Kinder Arco Iris", "Jardín Los Patitos", "Centro Infantil Sol",
    "Kinder Las Estrellitas", "Jardín Pequeños Genios", "Kinder El Castillo",
    "Centro Infantil Rayito de Luna", "Kinder Los Angelitos", "Jardín Semillitas",
    "Kinder Mundo Mágico", "Centro Infantil Colores", "Kinder La Casita Feliz",
    "Jardín Arcoíris", "Kinder Mis Primeros Pasos", "Centro Infantil Dulces Sueños",
    "Kinder El Jardín de los Niños", "Jardín Gotitas de Amor", "Kinder Carrusel",
    "Centro Infantil Hormiguitas", "Kinder Sueños y Colores"
]

# Nombres bolivianos para niños
NOMBRES_NINOS = ["Carlos", "Sofía", "Mateo", "Valentina", "Lucas", "Emma", "Diego", "Isabella", 
                 "Santiago", "Camila", "Sebastián", "María", "Nicolás", "Ana", "Gabriel",
                 "Juan", "Andrea", "Miguel", "Laura", "Pedro", "Carmen", "José"]

APELLIDOS = ["López", "García", "Rodríguez", "Pérez", "Martínez", "Sánchez", "González", 
             "Fernández", "Díaz", "Torres", "Ramírez", "Flores", "Morales", "Castro",
             "Mendoza", "Romero", "Silva", "Vargas", "Herrera", "Medina"]

# Calles de Santa Cruz
CALLES = ["Av. Monseñor Rivero", "Calle Junín", "Av. Cristo Redentor", "Calle Libertad",
          "Av. Irala", "Calle Sucre", "Av. Roca y Coronado", "Calle Warnes",
          "Av. Santos Dumont", "Calle 24 de Septiembre", "Av. Banzer", "Calle Velasco",
          "Av. Busch", "Calle Ayacucho", "Av. Alemana", "Calle Aroma"]

# ============================================================================
# GENERADORES
# ============================================================================

def generar_sql_kinders():
    """Genera SQL para insertar kinders con polígonos de área segura"""
    
    sql_statements = []
    
    for i, nombre in enumerate(NOMBRES_KINDERS, 1):
        zona = random.choice(ZONAS_SANTA_CRUZ)
        
        # Generar polígono cuadrado de ~100x100 metros alrededor del punto
        lat_base = zona["lat"] + random.uniform(-0.005, 0.005)
        lng_base = zona["lng"] + random.uniform(-0.005, 0.005)
        
        # Crear polígono (100m ≈ 0.001 grados)
        margen = 0.0008
        poligono = f"""ST_GeomFromText('POLYGON((
            {lng_base} {lat_base},
            {lng_base + margen} {lat_base},
            {lng_base + margen} {lat_base + margen},
            {lng_base} {lat_base + margen},
            {lng_base} {lat_base}
        ))', 4326)"""
        
        codigo = f"K{zona['nombre'][:3].upper()}{i:03d}"
        direccion = f"{random.choice(CALLES)} #{random.randint(100, 999)}, {zona['nombre']}"
        telefono = f"+591 3 {random.randint(3000000, 3999999)}"
        email = f"{nombre.lower().replace(' ', '')}@kinders.edu.bo"
        
        sql = f"""
-- Kinder {i}: {nombre} - {zona['nombre']}
INSERT INTO gis_tracking_centroeducativo (
    nombre, codigo, direccion, ciudad, departamento, telefono, email, area_segura, activo
) VALUES (
    '{nombre} - {zona["nombre"]}',
    '{codigo}',
    '{direccion}',
    'Santa Cruz de la Sierra',
    'Santa Cruz',
    '{telefono}',
    '{email}',
    {poligono},
    true
);"""
        sql_statements.append(sql)
    
    return "\n".join(sql_statements)


def generar_sql_tutores():
    """Genera SQL para insertar usuarios y tutores"""
    
    sql_statements = []
    
    for i in range(1, CANTIDAD_NINOS + 1):
        # Crear usuario
        username = f"tutor{i:03d}"
        # Django password hasher para '12345678'
        password = "pbkdf2_sha256$600000$xvKfKZzqBM2G0Qj0Dj5qE1$jH1V0hXqYqK5xZ8WxGrM3vF2oE9nC4aB6sD7fT8gH="
        
        nombre = random.choice(NOMBRES_NINOS)
        apellido = random.choice(APELLIDOS)
        telefono = f"+591 7{random.randint(1000000, 9999999)}"
        email = f"{nombre.lower()}.{apellido.lower()}{i}@email.com"
        
        sql_usuario = f"""
-- Usuario tutor {i}
INSERT INTO core_usuario (
    password, last_login, is_superuser, username, first_name, last_name,
    email, is_staff, is_active, date_joined, tipo_usuario, telefono
) VALUES (
    '{password}',
    NULL,
    false,
    '{username}',
    '{nombre}',
    '{apellido}',
    '{email}',
    false,
    true,
    NOW(),
    'TUTOR',
    '{telefono}'
);"""
        
        # Crear tutor vinculado al usuario
        relacion = random.choice(['Madre', 'Padre', 'Abuela', 'Abuelo', 'Tía', 'Tío'])
        ci = f"{random.randint(1000000, 9999999)}"
        telefono_emergencia = f"+591 6{random.randint(1000000, 9999999)}"
        
        sql_tutor = f"""
-- Tutor {i}: {nombre} {apellido}
INSERT INTO core_tutor (
    usuario_id, relacion, ci, telefono_emergencia
) VALUES (
    (SELECT id FROM core_usuario WHERE username = '{username}'),
    '{relacion}',
    '{ci}',
    '{telefono_emergencia}'
);"""
        
        sql_statements.append(sql_usuario)
        sql_statements.append(sql_tutor)
    
    return "\n".join(sql_statements)


def generar_sql_ninos():
    """Genera SQL para insertar niños"""
    
    sql_statements = []
    
    for i in range(1, CANTIDAD_NINOS + 1):
        nombre = random.choice(NOMBRES_NINOS)
        apellido_p = random.choice(APELLIDOS)
        apellido_m = random.choice(APELLIDOS)
        
        # Edad entre 3 y 5 años
        edad = random.randint(3, 5)
        fecha_nac = (datetime.now() - timedelta(days=edad*365 + random.randint(0, 364))).date()
        
        sexo = random.choice(['M', 'F'])
        
        # Asignar a un kinder aleatorio (del 1 al 20)
        kinder_id = random.randint(1, min(CANTIDAD_KINDERS, 20))
        
        # Asignar tutor (del 1 al número actual)
        tutor_id = i  # Cada niño tiene su propio tutor
        
        sql = f"""
-- Niño {i}: {nombre} {apellido_p} {apellido_m}
INSERT INTO gis_tracking_nino (
    nombre, apellido_paterno, apellido_materno, fecha_nacimiento, sexo,
    centro_educativo_id, tutor_principal_id, activo, tracking_activo, dispositivo_id
) VALUES (
    '{nombre}',
    '{apellido_p}',
    '{apellido_m}',
    '{fecha_nac}',
    '{sexo}',
    {kinder_id},
    {tutor_id},
    true,
    true,
    'device_{i:03d}_{nombre.lower()}'
);"""
        sql_statements.append(sql)
    
    return "\n".join(sql_statements)


def generar_sql_posiciones():
    """Genera SQL para insertar posiciones GPS históricas"""
    
    sql_statements = []
    
    for nino_id in range(1, CANTIDAD_NINOS + 1):
        # Generar posiciones para los últimos días
        for j in range(POSICIONES_POR_NINO):
            # Timestamp aleatorio en los últimos 7 días
            dias_atras = random.randint(0, 7)
            horas_atras = random.randint(0, 23)
            timestamp = datetime.now() - timedelta(days=dias_atras, hours=horas_atras)
            
            # Posición aleatoria en Santa Cruz
            zona = random.choice(ZONAS_SANTA_CRUZ)
            lat = zona["lat"] + random.uniform(-0.01, 0.01)
            lng = zona["lng"] + random.uniform(-0.01, 0.01)
            
            # Parámetros GPS
            bateria = random.randint(20, 100)
            dentro_area = random.choice([True, True, True, False])  # 75% dentro
            velocidad = random.uniform(0, 5) if random.random() < 0.8 else random.uniform(5, 15)
            precision = random.uniform(3, 20)
            
            sql = f"""
-- Posición GPS - Niño {nino_id} - {timestamp.strftime('%Y-%m-%d %H:%M')}
INSERT INTO gis_tracking_posiciongps (
    nino_id, ubicacion, timestamp, nivel_bateria, dentro_area_segura,
    velocidad_kmh, precision_metros
) VALUES (
    {nino_id},
    ST_GeomFromText('POINT({lng} {lat})', 4326),
    '{timestamp.isoformat()}',
    {bateria},
    {str(dentro_area).lower()},
    {velocidad:.1f},
    {precision:.1f}
);"""
            sql_statements.append(sql)
    
    return "\n".join(sql_statements)


# ============================================================================
# SCRIPT PRINCIPAL
# ============================================================================

def main():
    """Genera el archivo SQL completo"""
    
    print("="*70)
    print("🏗️  GENERADOR DE DATOS MASIVOS DE PRUEBA")
    print("="*70)
    print()
    print(f"📊 Configuración:")
    print(f"   • Kinders: {CANTIDAD_KINDERS}")
    print(f"   • Niños: {CANTIDAD_NINOS}")
    print(f"   • Posiciones por niño: {POSICIONES_POR_NINO}")
    print(f"   • Total posiciones GPS: {CANTIDAD_NINOS * POSICIONES_POR_NINO}")
    print()
    
    # Generar SQL
    print("🔧 Generando SQL...")
    
    sql_completo = f"""
-- ============================================================================
-- DATOS MASIVOS DE PRUEBA - Sistema Monitor Infantil SIG
-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- ============================================================================
-- 
-- Este script crea:
--   • {CANTIDAD_KINDERS} centros educativos (kinders)
--   • {CANTIDAD_NINOS} usuarios tutores
--   • {CANTIDAD_NINOS} niños
--   • {CANTIDAD_NINOS * POSICIONES_POR_NINO} posiciones GPS
--
-- IMPORTANTE: Ejecutar en el servidor con:
--   psql -U usuario -d nombre_db -f datos_masivos.sql
--
-- ============================================================================

BEGIN;

-- ============================================================================
-- 1. CENTROS EDUCATIVOS (KINDERS)
-- ============================================================================

{generar_sql_kinders()}

-- ============================================================================
-- 2. USUARIOS Y TUTORES
-- ============================================================================

{generar_sql_tutores()}

-- ============================================================================
-- 3. NIÑOS
-- ============================================================================

{generar_sql_ninos()}

-- ============================================================================
-- 4. POSICIONES GPS
-- ============================================================================

{generar_sql_posiciones()}

COMMIT;

-- ============================================================================
-- VERIFICACIÓN
-- ============================================================================

SELECT 'Centros Educativos: ' || COUNT(*) FROM gis_tracking_centroeducativo;
SELECT 'Usuarios Tutores: ' || COUNT(*) FROM core_usuario WHERE tipo_usuario = 'TUTOR';
SELECT 'Tutores: ' || COUNT(*) FROM core_tutor;
SELECT 'Niños: ' || COUNT(*) FROM gis_tracking_nino;
SELECT 'Posiciones GPS: ' || COUNT(*) FROM gis_tracking_posiciongps;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
"""
    
    # Guardar archivo
    filename = "datos_masivos.sql"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(sql_completo)
    
    print(f"✅ Archivo generado: {filename}")
    print()
    print("📋 Pasos siguientes:")
    print()
    print("1️⃣  Copiar archivo al servidor:")
    print(f"   scp {filename} root@monitor-infantil-backend:/tmp/")
    print()
    print("2️⃣  Conectar al servidor:")
    print("   ssh root@monitor-infantil-backend")
    print()
    print("3️⃣  Ejecutar SQL:")
    print("   cd /opt/monitor-infantil-sig/backend")
    print("   source venv/bin/activate")
    print(f"   python manage.py dbshell < /tmp/{filename}")
    print()
    print("4️⃣  Verificar:")
    print("   python manage.py shell << 'EOF'")
    print("   from apps.gis_tracking.models import *")
    print("   print(f'Kinders: {CentroEducativo.objects.count()}')")
    print("   print(f'Niños: {Nino.objects.count()}')")
    print("   print(f'Posiciones: {PosicionGPS.objects.count()}')")
    print("   EOF")
    print()
    print("="*70)
    print("✅ LISTO!")
    print("="*70)

if __name__ == "__main__":
    main()
