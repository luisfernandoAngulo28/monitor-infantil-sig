import psycopg2

# Credenciales de DigitalOcean
DB_CONFIG = {
    'host': 'monitor-infantil-db-do-user-22120002-0.h.db.ondigitalocean.com',
    'port': 25060,
    'database': 'monitor_infantil',
    'user': 'doadmin',
    'password': 'AVNS_Br2oEVoPiwxrqe4aM29',
    'sslmode': 'require'
}

try:
    print("Conectando a la base de datos...")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("Habilitando extensión PostGIS...")
    cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    
    print("Verificando PostGIS...")
    cursor.execute("SELECT PostGIS_version();")
    version = cursor.fetchone()
    print(f"✅ PostGIS habilitado correctamente: {version[0]}")
    
    cursor.close()
    conn.close()
    print("\n✅ ¡Base de datos lista para usar!")
    
except Exception as e:
    print(f"❌ Error: {e}")
