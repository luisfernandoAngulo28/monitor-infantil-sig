# 🚀 Mejoras Propuestas - Inspiradas en el Clon de Uber/InDriver

**Proyecto**: Monitor Infantil SIG  
**Fecha**: 7 de diciembre de 2025  
**Objetivo**: Integrar características profesionales del clon de Uber al proyecto académico

---

## 📊 ANÁLISIS: ¿Qué tiene el clon de Uber que NO tienes?

### ✅ Ya implementado en tu proyecto:
- GeoDjango + PostGIS ✅
- JWT Authentication ✅
- Google Maps ✅
- Firebase Push Notifications ✅
- GPS Tracking ✅
- Flutter App ✅
- REST API ✅

### 🆕 Características nuevas que puedes agregar:

---

## 1. 📍 BÚSQUEDA DE NIÑOS CERCANOS (ST_Distance_Sphere)

### **Qué hace el clon de Uber:**
```python
# Busca conductores cercanos en un radio de 5km
query = """
    SELECT id_driver, ST_Distance_Sphere(position, ST_GeomFromText('POINT(%s %s)', 4326)) AS distance
    FROM drivers_position
    HAVING distance <= 5000
"""
```

### **Cómo aplicarlo a Monitor Infantil:**

**Caso de Uso**: Buscar niños cerca de un kinder en un radio de 500m (útil para administradores)

#### **Backend - Nuevo Endpoint**

```python
# backend/apps/api/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import connection
import re

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_nearby_children(request, lat, lng, radius_meters=500):
    """
    Obtener niños cercanos a una ubicación específica
    
    Parámetros:
    - lat: Latitud del centro de búsqueda
    - lng: Longitud del centro de búsqueda  
    - radius_meters: Radio de búsqueda en metros (default 500m)
    
    Ejemplo:
    GET /api/ninos-cercanos/17.7833/-63.1821/?radius=1000
    """
    try:
        lat = float(lat)
        lng = float(lng)
        radius = int(request.GET.get('radius', radius_meters))
        
        query = """
            SELECT
                n.id,
                n.nombre,
                n.apellido,
                ST_AsText(p.ubicacion) AS ubicacion,
                ST_Distance_Sphere(
                    p.ubicacion, 
                    ST_GeomFromText('POINT(%s %s)', 4326)
                ) AS distancia_metros,
                p.timestamp,
                p.dentro_area_segura,
                ce.nombre AS kinder_nombre
            FROM
                gis_tracking_nino n
            INNER JOIN
                gis_tracking_posiciongps p ON n.id = p.nino_id
            INNER JOIN
                gis_tracking_centroeducativo ce ON n.centro_educativo_id = ce.id
            WHERE
                p.timestamp = (
                    SELECT MAX(timestamp) 
                    FROM gis_tracking_posiciongps 
                    WHERE nino_id = n.id
                )
            HAVING
                distancia_metros <= %s
            ORDER BY
                distancia_metros ASC
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [lng, lat, radius])
            rows = cursor.fetchall()
        
        ninos_cercanos = []
        for row in rows:
            # Parsear la geometría POINT(lng lat)
            position_text = row[3]
            match = re.match(r'POINT\(([-\d.]+) ([-\d.]+)\)', position_text)
            
            if match:
                lng_nino = float(match.group(1))
                lat_nino = float(match.group(2))
                
                ninos_cercanos.append({
                    'id': row[0],
                    'nombre_completo': f"{row[1]} {row[2]}",
                    'posicion': {
                        'lat': lat_nino,
                        'lng': lng_nino
                    },
                    'distancia_metros': round(row[4], 2),
                    'distancia_km': round(row[4] / 1000, 3),
                    'ultima_actualizacion': row[5],
                    'dentro_area_segura': row[6],
                    'kinder': row[7],
                    'estado': '🟢 Seguro' if row[6] else '🔴 Fuera del área'
                })
        
        return Response({
            'centro_busqueda': {'lat': lat, 'lng': lng},
            'radio_metros': radius,
            'total_encontrados': len(ninos_cercanos),
            'ninos': ninos_cercanos
        }, status=200)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)
```

#### **URLs**

```python
# backend/config/urls.py

from apps.api.views import get_nearby_children

urlpatterns = [
    # ... otras rutas
    path('api/ninos-cercanos/<str:lat>/<str:lng>/', get_nearby_children, name='ninos_cercanos'),
]
```

#### **Flutter - Pantalla de búsqueda**

```dart
// lib/screens/nearby_children_screen.dart

import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import '../services/api_service.dart';

class NearbyChildrenScreen extends StatefulWidget {
  @override
  _NearbyChildrenScreenState createState() => _NearbyChildrenScreenState();
}

class _NearbyChildrenScreenState extends State<NearbyChildrenScreen> {
  GoogleMapController? _mapController;
  List<Marker> _markers = [];
  LatLng _searchCenter = LatLng(-17.7833, -63.1821); // Santa Cruz
  double _radius = 1000; // 1km
  
  @override
  void initState() {
    super.initState();
    _searchNearbyChildren();
  }
  
  Future<void> _searchNearbyChildren() async {
    try {
      final response = await ApiService().getNearbyChildren(
        _searchCenter.latitude,
        _searchCenter.longitude,
        _radius.toInt(),
      );
      
      setState(() {
        _markers.clear();
        
        // Marcador del centro de búsqueda
        _markers.add(Marker(
          markerId: MarkerId('search_center'),
          position: _searchCenter,
          icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueBlue),
          infoWindow: InfoWindow(title: 'Centro de búsqueda'),
        ));
        
        // Marcadores de niños encontrados
        for (var nino in response['ninos']) {
          _markers.add(Marker(
            markerId: MarkerId('nino_${nino['id']}'),
            position: LatLng(
              nino['posicion']['lat'],
              nino['posicion']['lng'],
            ),
            icon: nino['dentro_area_segura']
                ? BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueGreen)
                : BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueRed),
            infoWindow: InfoWindow(
              title: nino['nombre_completo'],
              snippet: '${nino['distancia_metros']}m - ${nino['estado']}',
            ),
          ));
        }
      });
      
      // Mostrar resumen
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Encontrados ${response['total_encontrados']} niños en ${_radius}m'
          ),
        ),
      );
      
    } catch (e) {
      print('Error buscando niños cercanos: $e');
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Niños Cercanos'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: _searchNearbyChildren,
          ),
        ],
      ),
      body: Column(
        children: [
          // Control de radio
          Padding(
            padding: EdgeInsets.all(16),
            child: Row(
              children: [
                Text('Radio: ${_radius.toInt()}m'),
                Expanded(
                  child: Slider(
                    value: _radius,
                    min: 100,
                    max: 5000,
                    divisions: 49,
                    label: '${_radius.toInt()}m',
                    onChanged: (value) {
                      setState(() {
                        _radius = value;
                      });
                    },
                    onChangeEnd: (value) {
                      _searchNearbyChildren();
                    },
                  ),
                ),
              ],
            ),
          ),
          
          // Mapa
          Expanded(
            child: GoogleMap(
              initialCameraPosition: CameraPosition(
                target: _searchCenter,
                zoom: 14,
              ),
              markers: Set<Marker>.of(_markers),
              circles: {
                Circle(
                  circleId: CircleId('search_radius'),
                  center: _searchCenter,
                  radius: _radius,
                  fillColor: Colors.blue.withOpacity(0.2),
                  strokeColor: Colors.blue,
                  strokeWidth: 2,
                ),
              },
              onMapCreated: (controller) {
                _mapController = controller;
              },
              onTap: (position) {
                setState(() {
                  _searchCenter = position;
                });
                _searchNearbyChildren();
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

---

## 2. 🎨 WIDGETS PERSONALIZADOS PROFESIONALES

### **Widgets del clon de Uber que puedes integrar:**

#### **1. CustomButton (Botón estilizado)**

```dart
// lib/widgets/custom_button.dart

import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final Color color;
  final Color textColor;
  final EdgeInsetsGeometry margin;
  final double? width;
  final double height;
  final IconData? iconData;
  final Color iconColor;

  const CustomButton({
    Key? key,
    required this.text,
    required this.onPressed,
    this.color = const Color(0xFF2196F3),
    this.textColor = Colors.white,
    this.margin = const EdgeInsets.symmetric(horizontal: 40, vertical: 10),
    this.height = 50,
    this.width,
    this.iconData,
    this.iconColor = Colors.white,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: height,
      width: width ?? MediaQuery.of(context).size.width,
      margin: margin,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: color,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
          elevation: 5,
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (iconData != null) ...[
              Icon(iconData, color: iconColor, size: 28),
              SizedBox(width: 10),
            ],
            Text(
              text,
              style: TextStyle(
                color: textColor,
                fontSize: 18,
                fontWeight: FontWeight.bold,
                letterSpacing: 1,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

**Uso en tu proyecto:**

```dart
// En lugar de esto:
ElevatedButton(
  onPressed: _login,
  child: Text('Iniciar Sesión'),
)

// Usa esto:
CustomButton(
  text: 'Iniciar Sesión',
  onPressed: _login,
  iconData: Icons.login,
  color: Colors.green,
)
```

---

#### **2. CustomTextField (Campo de texto mejorado)**

```dart
// lib/widgets/custom_text_field.dart

import 'package:flutter/material.dart';

class CustomTextField extends StatelessWidget {
  final String label;
  final String? initialValue;
  final Function(String) onChanged;
  final IconData icon;
  final EdgeInsetsGeometry margin;
  final String? Function(String?)? validator;
  final Color backgroundColor;
  final TextInputType keyboardType;
  final bool obscureText;

  const CustomTextField({
    Key? key,
    required this.label,
    required this.icon,
    required this.onChanged,
    this.margin = const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
    this.validator,
    this.backgroundColor = Colors.white,
    this.initialValue,
    this.keyboardType = TextInputType.text,
    this.obscureText = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 60,
      margin: margin,
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(15),
        boxShadow: [
          BoxShadow(
            color: Colors.black12,
            blurRadius: 10,
            offset: Offset(0, 5),
          ),
        ],
      ),
      child: TextFormField(
        onChanged: onChanged,
        obscureText: obscureText,
        style: TextStyle(fontSize: 16, color: Colors.black87),
        initialValue: initialValue,
        validator: validator,
        keyboardType: keyboardType,
        decoration: InputDecoration(
          labelText: label,
          labelStyle: TextStyle(fontSize: 14, color: Colors.grey[600]),
          border: InputBorder.none,
          contentPadding: EdgeInsets.symmetric(vertical: 15),
          prefixIcon: Container(
            margin: EdgeInsets.only(right: 10),
            decoration: BoxDecoration(
              border: Border(
                right: BorderSide(color: Colors.grey[300]!, width: 1),
              ),
            ),
            child: Icon(icon, color: Colors.blue, size: 24),
          ),
        ),
      ),
    );
  }
}
```

**Uso:**

```dart
CustomTextField(
  label: 'Correo Electrónico',
  icon: Icons.email,
  keyboardType: TextInputType.emailAddress,
  onChanged: (value) => _email = value,
  validator: (value) {
    if (value == null || !value.contains('@')) {
      return 'Ingrese un correo válido';
    }
    return null;
  },
)
```

---

#### **3. CustomIconBack (Botón de retroceso estilizado)**

```dart
// lib/widgets/custom_icon_back.dart

import 'package:flutter/material.dart';

class CustomIconBack extends StatelessWidget {
  final Color color;
  final EdgeInsetsGeometry? margin;

  const CustomIconBack({
    Key? key,
    this.color = Colors.white,
    this.margin,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.topLeft,
      margin: margin ?? EdgeInsets.only(top: 40, left: 10),
      child: IconButton(
        onPressed: () => Navigator.pop(context),
        icon: Icon(Icons.arrow_back_ios, size: 30, color: color),
        tooltip: 'Volver',
      ),
    );
  }
}
```

---

## 3. 🗺️ CÁLCULO DE RUTAS Y DISTANCIAS

### **Modelo para guardar tiempos y distancias**

```python
# backend/apps/gis_tracking/models.py

class RutaGuardada(models.Model):
    """Rutas desde un punto de origen hasta el kinder"""
    
    nino = models.ForeignKey(
        Nino,
        on_delete=models.CASCADE,
        related_name='rutas'
    )
    
    # Punto de origen (ej: casa del niño)
    origen = gis_models.PointField(srid=4326)
    origen_nombre = models.CharField(max_length=100, default='Casa')
    
    # Punto de destino (centro educativo)
    destino = gis_models.PointField(srid=4326)
    destino_nombre = models.CharField(max_length=100)
    
    # Datos calculados
    distancia_km = models.FloatField(
        help_text='Distancia en línea recta (km)'
    )
    distancia_real_km = models.FloatField(
        null=True,
        blank=True,
        help_text='Distancia por calles (Google Maps API)'
    )
    tiempo_estimado_minutos = models.IntegerField(
        null=True,
        blank=True,
        help_text='Tiempo estimado en auto (minutos)'
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Ruta Guardada'
        verbose_name_plural = 'Rutas Guardadas'
    
    def save(self, *args, **kwargs):
        # Calcular distancia en línea recta con PostGIS
        if self.origen and self.destino:
            from django.contrib.gis.measure import Distance
            self.distancia_km = round(
                self.origen.distance(self.destino) * 111,  # Conversión a km
                2
            )
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Ruta: {self.origen_nombre} → {self.destino_nombre} ({self.distancia_km}km)"
```

---

## 4. 📊 DASHBOARD ADMINISTRATIVO MEJORADO

### **Estadísticas en tiempo real**

```python
# backend/apps/api/views.py

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_stats(request):
    """
    Estadísticas generales del sistema para administradores
    """
    from django.db.models import Count, Avg
    from apps.gis_tracking.models import Nino, CentroEducativo, PosicionGPS
    from apps.alerts.models import Alerta
    from datetime import datetime, timedelta
    
    # Stats básicas
    total_ninos = Nino.objects.count()
    total_kinders = CentroEducativo.objects.count()
    
    # Niños activos (con GPS en últimos 5 min)
    hace_5_min = datetime.now() - timedelta(minutes=5)
    ninos_activos = PosicionGPS.objects.filter(
        timestamp__gte=hace_5_min
    ).values('nino').distinct().count()
    
    # Alertas hoy
    hoy = datetime.now().date()
    alertas_hoy = Alerta.objects.filter(
        fecha_hora__date=hoy
    ).count()
    
    # Alertas sin resolver
    alertas_pendientes = Alerta.objects.filter(
        resuelta=False
    ).count()
    
    # Niños fuera del área ahora
    ninos_fuera_area = Nino.objects.filter(
        posiciones_gps__dentro_area_segura=False,
        posiciones_gps__timestamp__gte=hace_5_min
    ).distinct().count()
    
    # Precisión promedio GPS
    precision_promedio = PosicionGPS.objects.filter(
        timestamp__gte=hace_5_min
    ).aggregate(Avg('precision'))['precision__avg']
    
    return Response({
        'resumen': {
            'total_ninos': total_ninos,
            'ninos_activos': ninos_activos,
            'total_kinders': total_kinders,
        },
        'alertas': {
            'hoy': alertas_hoy,
            'pendientes': alertas_pendientes,
        },
        'seguridad': {
            'ninos_seguros': ninos_activos - ninos_fuera_area,
            'ninos_fuera_area': ninos_fuera_area,
            'porcentaje_seguridad': round(
                ((ninos_activos - ninos_fuera_area) / ninos_activos * 100) 
                if ninos_activos > 0 else 100, 
                2
            ),
        },
        'gps': {
            'precision_promedio_metros': round(precision_promedio or 0, 2),
        },
        'timestamp': datetime.now().isoformat(),
    })
```

---

## 5. 🔔 SISTEMA DE NOTIFICACIONES MEJORADO

### **Tipos de notificaciones**

```python
# backend/apps/alerts/notifications.py

from firebase_admin import messaging

class NotificationService:
    """Servicio mejorado de notificaciones"""
    
    TIPOS_ALERTA = {
        'SALIDA_AREA': {
            'titulo': '🚨 Alerta de Seguridad',
            'icono': 'warning',
            'prioridad': 'high',
            'sonido': 'alarma.mp3',
        },
        'VELOCIDAD_ALTA': {
            'titulo': '⚠️ Velocidad Anormal',
            'icono': 'speed',
            'prioridad': 'high',
            'sonido': 'alerta.mp3',
        },
        'BATERIA_BAJA': {
            'titulo': '🔋 Batería Baja',
            'icono': 'battery',
            'prioridad': 'normal',
            'sonido': 'default',
        },
        'REGRESO_AREA': {
            'titulo': '✅ Regresó al Área Segura',
            'icono': 'check_circle',
            'prioridad': 'normal',
            'sonido': 'success.mp3',
        },
    }
    
    @staticmethod
    def enviar_notificacion_personalizada(
        fcm_token: str,
        tipo: str,
        nino_nombre: str,
        mensaje_extra: str = '',
        data: dict = None
    ):
        """Enviar notificación con configuración según el tipo"""
        
        config = NotificationService.TIPOS_ALERTA.get(
            tipo, 
            NotificationService.TIPOS_ALERTA['SALIDA_AREA']
        )
        
        mensaje_completo = f"{nino_nombre} - {mensaje_extra}"
        
        message = messaging.Message(
            notification=messaging.Notification(
                title=config['titulo'],
                body=mensaje_completo,
            ),
            data=data or {},
            android=messaging.AndroidConfig(
                priority=config['prioridad'],
                notification=messaging.AndroidNotification(
                    icon=config['icono'],
                    sound=config['sonido'],
                    channel_id='alertas_monitor_infantil',
                    color='#FF0000' if config['prioridad'] == 'high' else '#2196F3',
                ),
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound=config['sonido'],
                        badge=1,
                    ),
                ),
            ),
            token=fcm_token,
        )
        
        try:
            response = messaging.send(message)
            print(f'✅ Notificación enviada: {response}')
            return True
        except Exception as e:
            print(f'❌ Error enviando notificación: {e}')
            return False
```

---

## 6. 📈 MEJORAS DE RENDIMIENTO

### **Índices espaciales optimizados**

```python
# backend/apps/gis_tracking/migrations/0XXX_add_spatial_indexes.py

from django.contrib.gis.db.models import Extent
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('gis_tracking', '0XXX_previous_migration'),
    ]

    operations = [
        migrations.RunSQL(
            # Índice espacial GiST en posiciones GPS
            """
            CREATE INDEX idx_posicion_gps_ubicacion_gist 
            ON gis_tracking_posiciongps 
            USING GIST (ubicacion);
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_posicion_gps_ubicacion_gist;
            """
        ),
        migrations.RunSQL(
            # Índice en timestamp para consultas temporales
            """
            CREATE INDEX idx_posicion_gps_timestamp 
            ON gis_tracking_posiciongps (timestamp DESC);
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_posicion_gps_timestamp;
            """
        ),
        migrations.RunSQL(
            # Índice compuesto para búsquedas frecuentes
            """
            CREATE INDEX idx_posicion_gps_nino_timestamp 
            ON gis_tracking_posiciongps (nino_id, timestamp DESC);
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_posicion_gps_nino_timestamp;
            """
        ),
    ]
```

---

## 📝 RESUMEN DE MEJORAS PROPUESTAS

| # | Mejora | Dificultad | Tiempo | Impacto | Prioridad |
|---|--------|-----------|--------|---------|-----------|
| 1 | Búsqueda de niños cercanos (ST_Distance) | Media | 2h | Alto | ⭐⭐⭐ |
| 2 | Widgets personalizados | Baja | 1h | Medio | ⭐⭐ |
| 3 | Modelo de rutas y distancias | Media | 2h | Medio | ⭐⭐ |
| 4 | Dashboard con estadísticas | Media | 3h | Alto | ⭐⭐⭐ |
| 5 | Notificaciones tipificadas | Baja | 1h | Alto | ⭐⭐⭐ |
| 6 | Índices espaciales optimizados | Baja | 30min | Alto | ⭐⭐⭐ |

**Total estimado**: 9.5 horas de desarrollo

---

## 🎯 PLAN DE IMPLEMENTACIÓN (Orden sugerido)

### **Fase 1: Quick Wins (2 horas)**
1. ✅ Widgets personalizados (30 min)
2. ✅ Índices espaciales (30 min)
3. ✅ Notificaciones tipificadas (1 hora)

### **Fase 2: Features Importantes (4 horas)**
4. ✅ Búsqueda de niños cercanos (2 horas)
5. ✅ Dashboard de estadísticas (2 horas)

### **Fase 3: Extras (3.5 horas)**
6. ✅ Modelo de rutas (2 horas)
7. ✅ Integración Google Maps Directions API (1.5 horas)

---

## 🚀 CÓMO EMPEZAR

### **Paso 1: Widgets (30 minutos)**

```bash
# Crear carpeta de widgets reutilizables
cd mobile/monitor_infantil_app/lib
mkdir -p widgets

# Crear los 3 widgets
# - custom_button.dart
# - custom_text_field.dart
# - custom_icon_back.dart
```

### **Paso 2: Búsqueda cercanos (2 horas)**

```bash
# Backend
cd backend/apps/api
# Agregar vista get_nearby_children a views.py
# Agregar ruta en config/urls.py

# Flutter
cd mobile/monitor_infantil_app/lib/screens
# Crear nearby_children_screen.dart
# Agregar método en api_service.dart
```

### **Paso 3: Dashboard (2 horas)**

```bash
# Backend
# Agregar vista get_dashboard_stats en apps/api/views.py

# Flutter
# Crear dashboard_screen.dart con gráficos
flutter pub add fl_chart  # Para gráficos
```

---

## 💡 VALOR AGREGADO PARA TU PROYECTO

Con estas mejoras, tu proyecto tendrá:

1. **Funcionalidad profesional** comparable a apps comerciales
2. **Análisis espacial avanzado** (ST_Distance_Sphere)
3. **UI/UX mejorada** con widgets reutilizables
4. **Dashboard administrativo** con métricas en tiempo real
5. **Sistema de notificaciones robusto** con tipos y prioridades
6. **Optimización de rendimiento** con índices espaciales

**Cumplimiento estimado**: De 104% a **115%** del enunciado 🏆

---

**Generado**: 7 de diciembre de 2025
