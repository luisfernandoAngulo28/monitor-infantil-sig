# Generated manually for performance optimization
# This migration adds spatial indexes to improve query performance

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gis_tracking', '0001_initial'),  # Ajustar al número de tu última migración
    ]

    operations = [
        # Índice espacial GiST en el campo 'ubicacion' de PosicionGPS
        # Mejora las consultas de Point-in-Polygon y ST_Distance
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_posicion_gps_ubicacion_gist 
            ON gis_tracking_posiciongps 
            USING GIST (ubicacion);
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_posicion_gps_ubicacion_gist;
            """
        ),
        
        # Índice espacial GiST en el campo 'area_segura' de CentroEducativo
        # Mejora las consultas de contención espacial
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_centro_educativo_area_gist 
            ON gis_tracking_centroeducativo 
            USING GIST (area_segura);
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_centro_educativo_area_gist;
            """
        ),
        
        # Índice en timestamp para consultas temporales (últimas posiciones)
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_posicion_gps_timestamp 
            ON gis_tracking_posiciongps (timestamp DESC);
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_posicion_gps_timestamp;
            """
        ),
        
        # Índice compuesto para búsquedas frecuentes (niño + timestamp)
        # Útil para obtener la última posición de un niño específico
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_posicion_gps_nino_timestamp 
            ON gis_tracking_posiciongps (nino_id, timestamp DESC);
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_posicion_gps_nino_timestamp;
            """
        ),
        
        # Índice en campo 'dentro_area_segura' para filtros rápidos
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_posicion_gps_dentro_area 
            ON gis_tracking_posiciongps (dentro_area_segura) 
            WHERE dentro_area_segura = FALSE;
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_posicion_gps_dentro_area;
            """
        ),
        
        # Índice para alertas no resueltas
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_alerta_resuelta 
            ON alerts_alerta (resuelta, fecha_hora DESC) 
            WHERE resuelta = FALSE;
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_alerta_resuelta;
            """
        ),
    ]
