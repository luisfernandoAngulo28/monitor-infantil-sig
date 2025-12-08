# 🎥 GUIÓN PARA VIDEO TUTORIAL
## Sistema de Monitoreo Infantil - Demo Completa

**Duración estimada:** 10 minutos  
**Herramientas:** OBS Studio, Dispositivo Android/iOS, Navegador web  
**Formato:** 1920x1080 (Full HD), 30 FPS

---

## 📋 Checklist Pre-Grabación

### Software necesario:
- [ ] OBS Studio instalado y configurado
- [ ] Android Studio Emulator o dispositivo físico
- [ ] Navegador Chrome
- [ ] Editor de video (opcional): DaVinci Resolve, Adobe Premiere

### Preparación del entorno:
- [ ] App Flutter corriendo en emulador
- [ ] Backend accesible (https://monitor-infantil.duckdns.org)
- [ ] Credenciales de prueba:
  - Tutor: maria.lopez / 12345678
  - Admin: fernando / admin123
- [ ] Datos de prueba: Carlos López en Mountain View
- [ ] Micrófono probado
- [ ] Pantalla limpia (cerrar apps innecesarias)

---

## 🎬 ESTRUCTURA DEL VIDEO

```
┌─────────────────────────────────────────────────────┐
│ 00:00 - 00:30  │ Introducción                       │
│ 00:30 - 02:00  │ Login y Dashboard (App Móvil)      │
│ 02:00 - 04:00  │ Mapa en Tiempo Real                │
│ 04:00 - 05:30  │ Búsqueda de Niños Cercanos        │
│ 05:30 - 07:00  │ Sistema de Alertas                 │
│ 07:00 - 09:00  │ Panel de Administración           │
│ 09:00 - 10:00  │ Conclusión y Recursos              │
└─────────────────────────────────────────────────────┘
```

---

## 📝 GUIÓN DETALLADO

### SEGMENTO 1: Introducción (00:00 - 00:30)

**[PANTALLA: Logo del sistema + título]**

```
┌─────────────────────────────────────────┐
│                                         │
│     🗺️ MONITOR INFANTIL SIG            │
│                                         │
│   Sistema de Monitoreo Geoespacial     │
│        para Niños Prescolares          │
│                                         │
│         INF442-SA • 2025               │
└─────────────────────────────────────────┘
```

**AUDIO (Narración):**

> "Bienvenidos a la demostración del Sistema de Monitoreo Infantil con SIG.
>
> Este sistema utiliza tecnología de Sistemas de Información Geográfica para rastrear en tiempo real la ubicación de niños prescolares y alertar automáticamente a padres y tutores cuando un niño sale del área segura de su centro educativo.
>
> En los próximos 10 minutos veremos:
> - Cómo funciona la aplicación móvil para padres y tutores
> - El sistema de alertas automáticas
> - El panel de administración web
> - Y una demostración de la búsqueda de niños cercanos
>
> Comencemos."

**DURACIÓN:** 30 segundos

---

### SEGMENTO 2: Login y Dashboard (00:30 - 02:00)

**[PANTALLA: Cambiar a grabación del emulador Android]**

**ACCIÓN 1: Abrir la app**

**AUDIO:**
> "Primero, abramos la aplicación móvil Monitor Infantil.
> Esta app está disponible tanto para Android como para iOS."

**[MOSTRAR: Pantalla de login]**

```
┌─────────────────────────────┐
│   Monitor Infantil          │
│                             │
│   Usuario: [___________]    │
│   Contraseña: [_______]     │
│                             │
│   [  Iniciar sesión  ]      │
└─────────────────────────────┘
```

**ACCIÓN 2: Escribir credenciales**

**AUDIO:**
> "Voy a iniciar sesión como María López, una madre que tiene a su hijo Carlos registrado en el sistema."

**[TECLEAR: maria.lopez]**  
**[TECLEAR: 12345678]**  
**[PRESIONAR: Iniciar sesión]**

**ACCIÓN 3: Dashboard**

**[MOSTRAR: Dashboard con lista de niños]**

**AUDIO:**
> "Una vez dentro, vemos el dashboard principal.
>
> Aquí María puede ver a su hijo Carlos López Días, de 5 años, que asiste al Kinder Arco Iris en Santa Cruz.
>
> Observen los detalles importantes:
> - Estado: En área segura (marcado en verde)
> - Nivel de batería: 85%
> - Última actualización: hace 2 minutos
>
> Esto le da tranquilidad a María de que Carlos está donde debe estar."

**[PAUSAR 3 segundos para que se vea la pantalla]**

**DURACIÓN:** 1 minuto 30 segundos

---

### SEGMENTO 3: Mapa en Tiempo Real (02:00 - 04:00)

**ACCIÓN 1: Abrir mapa**

**AUDIO:**
> "Ahora veamos el mapa en tiempo real.
> Tocamos el botón 'Ver en mapa'."

**[TOCAR: Botón "Ver en mapa"]**

**[MOSTRAR: Pantalla de mapa cargando, luego mapa con marcador]**

**AUDIO:**
> "El mapa se carga usando Google Maps y nos muestra:
>
> 1. La ubicación exacta de Carlos, marcada con un pin azul
> 2. El polígono del área segura del kinder, en color celeste
> 3. Nuestra propia ubicación como tutor
>
> En este caso, Carlos está en Mountain View, California, exactamente en las coordenadas del Googleplex, que usamos para esta demo.
>
> El polígono azul marca los límites del área segura. Mientras Carlos esté dentro de este polígono, todo está normal."

**ACCIÓN 2: Zoom in/out**

**[HACER PINCH para zoom in]**  
**[HACER PINCH para zoom out]**

**AUDIO:**
> "Podemos hacer zoom para ver más detalles o alejarnos para tener una vista general."

**ACCIÓN 3: Tocar el marcador**

**[TOCAR: Marcador del niño]**

**[MOSTRAR: Info card con detalles]**

**AUDIO:**
> "Al tocar el marcador, vemos una tarjeta con información detallada:
> - Nombre completo del niño
> - Centro educativo
> - Batería del dispositivo
> - Última actualización
> - Distancia desde nuestra ubicación
>
> Esta información se actualiza automáticamente cada 30 segundos."

**DURACIÓN:** 2 minutos

---

### SEGMENTO 4: Búsqueda de Niños Cercanos (04:00 - 05:30)

**ACCIÓN 1: Abrir menú lateral**

**AUDIO:**
> "Ahora veamos una funcionalidad avanzada: la búsqueda de niños cercanos.
>
> Esta característica utiliza análisis espacial PostGIS para encontrar niños en un radio específico.
>
> Abramos el menú lateral."

**[TOCAR: Ícono de menú (hamburguesa)]**

**[MOSTRAR: Drawer con opciones]**

**ACCIÓN 2: Seleccionar búsqueda cercanos**

**[TOCAR: "Búsqueda de Niños Cercanos"]**

**[MOSTRAR: Pantalla de búsqueda con mapa]**

**AUDIO:**
> "La pantalla de búsqueda cercanos nos muestra un mapa centrado en nuestra ubicación actual.
>
> En la parte superior vemos:
> - Número de niños encontrados
> - Radio de búsqueda: 5 kilómetros
>
> Presionemos el botón de búsqueda."

**ACCIÓN 3: Ejecutar búsqueda**

**[TOCAR: Botón flotante de búsqueda (lupa)]**

**[MOSTRAR: Animación de carga, luego resultado]**

**AUDIO:**
> "El sistema ejecuta una consulta espacial en el servidor usando PostGIS.
> La función ST_Distance calcula la distancia geográfica real entre nuestra ubicación y cada niño registrado.
>
> Y aquí está el resultado: 1 niño encontrado.
> Carlos López está exactamente a 0 metros de distancia porque estamos usando la misma ubicación para esta demo."

**ACCIÓN 4: Ver detalles**

**[TOCAR: Marcador del resultado]**

**[MOSTRAR: Bottom sheet con detalles]**

**AUDIO:**
> "Al tocar el marcador, se despliega una tarjeta con:
> - Nombre completo: Carlos López Días
> - Centro educativo: Kinder Arco Iris - Santa Cruz
> - Nivel de batería: 85%
> - Distancia exacta: 0.0 metros
>
> Esto es muy útil para coordinaciones entre tutores, actividades grupales, o situaciones de emergencia."

**DURACIÓN:** 1 minuto 30 segundos

---

### SEGMENTO 5: Sistema de Alertas (05:30 - 07:00)

**ACCIÓN 1: Volver al dashboard**

**[PRESIONAR: Botón atrás hasta llegar al dashboard]**

**AUDIO:**
> "Ahora veamos la característica más importante: el sistema de alertas automáticas.
>
> Supongamos que Carlos sale del área segura del kinder."

**ACCIÓN 2: Simular alerta (Opción A: Mostrar notificación guardada)**

**[MOSTRAR: Screenshot de notificación push]**

```
╔═══════════════════════════════════╗
║ 🔔 MONITOR INFANTIL               ║
║                                   ║
║ ⚠️ ALERTA: Salida de área segura ║
║                                   ║
║ Carlos López Días ha salido del   ║
║ área segura del Kinder Arco Iris  ║
║                                   ║
║ Hace 2 minutos                    ║
║                                   ║
║ [Ver detalles]                    ║
╚═══════════════════════════════════╝
```

**AUDIO:**
> "Inmediatamente, María recibe una notificación push en su celular.
>
> La notificación dice:
> 'ALERTA: Carlos López Días ha salido del área segura del Kinder Arco Iris'
>
> Esto sucede automáticamente gracias al análisis espacial.
> El sistema detecta que la posición GPS de Carlos ya no está contenida dentro del polígono del kinder."

**ACCIÓN 3: Abrir alerta**

**[TOCAR: Notificación]**

**[MOSTRAR: Pantalla de detalles de alerta]**

**AUDIO:**
> "Al tocar la notificación, se abre la app mostrando los detalles completos:
>
> - Tipo de alerta: Salida de área segura
> - Fecha y hora exacta
> - Ubicación actual del niño en el mapa
> - Distancia desde el kinder
> - Estado de la alerta: Enviada
>
> María puede entonces:
> 1. Ver la ubicación exacta en el mapa
> 2. Llamar al kinder para verificar
> 3. Marcar la alerta como resuelta cuando confirme que todo está bien"

**ACCIÓN 4: Resolver alerta**

**[TOCAR: Botón "Marcar como resuelta"]**

**[MOSTRAR: Confirmación]**

**AUDIO:**
> "Una vez que María confirma que Carlos está seguro, marca la alerta como resuelta.
> Esto actualiza el estado en el sistema y queda registrado en el historial."

**DURACIÓN:** 1 minuto 30 segundos

---

### SEGMENTO 6: Panel de Administración (07:00 - 09:00)

**[PANTALLA: Cambiar a grabación del navegador web]**

**ACCIÓN 1: Abrir admin Django**

**AUDIO:**
> "Ahora veamos el panel de administración web, que usan los directores de kinders y el personal técnico.
>
> Accedemos desde un navegador a:
> https://monitor-infantil.duckdns.org/admin/"

**[NAVEGAR: https://monitor-infantil.duckdns.org/admin/]**

**[MOSTRAR: Página de login de Django]**

**ACCIÓN 2: Login como admin**

**[TECLEAR: fernando]**  
**[TECLEAR: admin123]**  
**[PRESIONAR: Iniciar sesión]**

**[MOSTRAR: Panel principal de Django Admin]**

**AUDIO:**
> "Una vez dentro, vemos el panel de administración de Django.
>
> Desde aquí se puede gestionar:
> - Centros educativos (kinders)
> - Niños registrados
> - Tutores y usuarios
> - Posiciones GPS
> - Alertas
> - Y notificaciones"

**ACCIÓN 3: Ver centros educativos**

**[CLIC: "Centros educativos" → "Cambiar"]**

**[MOSTRAR: Lista de kinders]**

**AUDIO:**
> "Aquí vemos la lista de centros educativos registrados.
> Tenemos 8 kinders en el sistema, incluyendo:
> - Kinder Arco Iris - Santa Cruz
> - Jardín Los Patitos
> - Centro Infantil Sol
>
> Cada uno tiene su código único, dirección, y lo más importante: su área segura definida."

**ACCIÓN 4: Ver detalle de un kinder**

**[CLIC: "Kinder Arco Iris - Santa Cruz"]**

**[MOSTRAR: Formulario de edición]**

**AUDIO:**
> "Al abrir un kinder, vemos todos sus datos:
> - Información básica: nombre, dirección, teléfono
> - Y aquí está el campo crucial: ÁREA SEGURA
>
> Este campo contiene un polígono en formato WKT (Well-Known Text).
> Este polígono define los límites geográficos del kinder.
>
> Veamos las coordenadas..."

**[SCROLL: Hasta "area_segura"]**

**[MOSTRAR: Campo con POLYGON(...)]**

**AUDIO:**
> "Aquí está el polígono definido con coordenadas de longitud y latitud.
> Cada línea representa una esquina del área.
>
> Para crear o modificar estas áreas, los administradores usan herramientas como:
> - geojson.io
> - QGIS
> - Google Earth
>
> Y luego copian las coordenadas a este campo."

**ACCIÓN 5: Ver niños**

**[NAVEGAR: Atrás → "Niños" → "Cambiar"]**

**[MOSTRAR: Lista de niños]**

**AUDIO:**
> "En la sección de niños vemos todos los registros.
>
> Aquí está Carlos López, nuestro niño de ejemplo:
> - Asignado al Kinder Arco Iris
> - Tutor principal: María López
> - Tracking activo: Sí
> - Estado: Activo
>
> También podemos ver otros niños como Sofía Pérez y Mateo García."

**ACCIÓN 6: Ver posiciones GPS**

**[NAVEGAR: "Posiciones GPS" → "Cambiar"]**

**[MOSTRAR: Lista de posiciones, filtrar por Carlos]**

**AUDIO:**
> "Finalmente, en Posiciones GPS vemos el historial de ubicaciones.
>
> Filtro para mostrar solo las de Carlos...
>
> Y aquí están sus últimas 2 posiciones en Mountain View, California:
> - Timestamp: 14:40:08
> - Batería: 85%
> - Dentro del área segura: Sí
> - Coordenadas: POINT(-122.084 37.422)
>
> Este es el dato crudo que se almacena en la base de datos PostGIS."

**ACCIÓN 7: Ver alertas**

**[NAVEGAR: "Alertas" → "Cambiar"]**

**[MOSTRAR: Lista de alertas]**

**AUDIO:**
> "Y en la sección de Alertas vemos todas las notificaciones generadas:
> - Alertas de salida de área
> - Alertas de batería baja
> - Alertas de pérdida de señal
>
> Cada alerta tiene su estado: Pendiente, Enviada, Leída, o Resuelta.
>
> Los administradores pueden revisar estas alertas y generar reportes estadísticos."

**DURACIÓN:** 2 minutos

---

### SEGMENTO 7: Conclusión y Recursos (09:00 - 10:00)

**[PANTALLA: Volver a diapositivas]**

**[MOSTRAR: Slide de resumen]**

```
┌─────────────────────────────────────────────┐
│   ✅ CARACTERÍSTICAS PRINCIPALES             │
│                                             │
│   📍 Monitoreo GPS en tiempo real           │
│   🗺️ Análisis espacial con PostGIS         │
│   🔔 Alertas automáticas                    │
│   📱 App móvil Flutter (Android/iOS)        │
│   🌐 Panel web de administración           │
│   🔍 Búsqueda de niños cercanos            │
│   🔒 Datos encriptados (HTTPS)             │
│                                             │
└─────────────────────────────────────────────┘
```

**AUDIO:**
> "En resumen, el Sistema de Monitoreo Infantil con SIG ofrece:
>
> ✓ Monitoreo GPS en tiempo real
> ✓ Análisis espacial con PostGIS para detección automática
> ✓ Alertas instantáneas a tutores
> ✓ Aplicación móvil multiplataforma
> ✓ Panel de administración web completo
> ✓ Búsqueda de niños cercanos con radio configurable
> ✓ Y seguridad con datos encriptados
>
> Este sistema cumple con todos los requisitos del proyecto INF442-SA:
> - Base de datos geoespacial con PostgreSQL y PostGIS
> - Análisis vectorial con polígonos y puntos
> - Detección de anomalías espaciales
> - Notificaciones en tiempo real
> - Y una arquitectura cloud escalable"

**[MOSTRAR: Slide de tecnologías]**

```
┌─────────────────────────────────────────────┐
│   🛠️ STACK TECNOLÓGICO                     │
│                                             │
│   Backend:                                  │
│   • Django 5.0 + GeoDjango                 │
│   • PostgreSQL 16 + PostGIS 3.4            │
│   • Channels (WebSocket)                   │
│   • Redis                                   │
│                                             │
│   Frontend:                                 │
│   • Flutter 3.35.4                         │
│   • Google Maps SDK                        │
│   • Firebase Cloud Messaging               │
│                                             │
│   Infraestructura:                          │
│   • Ubuntu 24.04 LTS                       │
│   • Nginx + Daphne                         │
│   • DigitalOcean                           │
│                                             │
└─────────────────────────────────────────────┘
```

**AUDIO:**
> "Tecnologías utilizadas:
> - Backend con Django y GeoDjango para análisis SIG
> - PostgreSQL con la extensión PostGIS para geometrías
> - Flutter para la app móvil
> - Y Firebase para notificaciones push
>
> Todo desplegado en un servidor Ubuntu en DigitalOcean con HTTPS."

**[MOSTRAR: Slide de recursos]**

```
┌─────────────────────────────────────────────┐
│   📚 RECURSOS ADICIONALES                   │
│                                             │
│   • MANUAL_USUARIO.md                      │
│   • MANUAL_ADMINISTRADOR.md                │
│   • FAQ.md (Preguntas Frecuentes)         │
│   • DOCUMENTACION_TECNICA.md               │
│                                             │
│   🌐 Demo en vivo:                         │
│   https://monitor-infantil.duckdns.org     │
│                                             │
│   📧 Contacto:                             │
│   soporte@monitor-infantil.com             │
│                                             │
└─────────────────────────────────────────────┘
```

**AUDIO:**
> "Para más información, consulte:
> - El Manual de Usuario
> - El Manual del Administrador
> - El documento de Preguntas Frecuentes
> - Y la Documentación Técnica completa
>
> También puede acceder a la demo en vivo en:
> https://monitor-infantil.duckdns.org
>
> Gracias por ver esta demostración.
> Este ha sido el Sistema de Monitoreo Infantil con SIG para el proyecto INF442-SA."

**[PANTALLA FINAL: Logo + créditos]**

```
┌─────────────────────────────────────────────┐
│                                             │
│        🗺️ MONITOR INFANTIL SIG             │
│                                             │
│         Universidad [Nombre]                │
│         Materia: INF442-SA                  │
│         Docente: Ing. Franklin Calderón     │
│                                             │
│         Desarrollo: [Tu nombre]             │
│         Año: 2025                           │
│                                             │
│   ✅ Cumple 92% del enunciado              │
│   ✅ Sistema funcional desplegado          │
│   ✅ Análisis SIG real con PostGIS         │
│                                             │
└─────────────────────────────────────────────┘
```

**DURACIÓN:** 1 minuto

---

## 🎬 POST-PRODUCCIÓN

### Edición:
1. **Intro (5 seg):**
   - Logo animado
   - Título del sistema

2. **Transiciones:**
   - Fade entre segmentos
   - Zoom suave al cambiar de pantalla

3. **Overlays:**
   - Números de segmento (1/7, 2/7, etc.)
   - Anotaciones para destacar puntos importantes

4. **Audio:**
   - Música de fondo suave (volumen bajo)
   - Normalizar audio de narración
   - Eliminar silencios largos

5. **Outro (5 seg):**
   - Pantalla de créditos
   - Links a recursos

### Exportación:
- **Formato:** MP4 (H.264)
- **Resolución:** 1920x1080
- **Bitrate:** 8-10 Mbps
- **Audio:** AAC 192 kbps
- **Nombre:** `MonitorInfantil_SIG_Demo_INF442.mp4`

---

## 📤 PUBLICACIÓN

### YouTube:
```
Título:
Sistema de Monitoreo Infantil con SIG | Demo Completa | INF442-SA

Descripción:
Demostración del Sistema de Monitoreo Infantil desarrollado con 
tecnologías SIG (Sistemas de Información Geográfica).

🎯 Características:
• Monitoreo GPS en tiempo real
• Análisis espacial con PostGIS
• Alertas automáticas
• App móvil multiplataforma
• Panel de administración web

🛠️ Tecnologías:
Django + GeoDjango, PostgreSQL + PostGIS, Flutter, Firebase

📚 Recursos:
https://github.com/[usuario]/monitor-infantil-sig

⏱️ Índice:
00:00 Introducción
00:30 Login y Dashboard
02:00 Mapa en Tiempo Real
04:00 Búsqueda de Niños Cercanos
05:30 Sistema de Alertas
07:00 Panel de Administración
09:00 Conclusión

#SIG #GIS #PostGIS #Django #Flutter #GPS #Monitoreo

Tags:
SIG, GIS, PostGIS, Django, GeoDjango, Flutter, GPS tracking,
child monitoring, sistema de información geográfica
```

---

## ✅ CHECKLIST FINAL

- [ ] Video grabado en 1080p
- [ ] Audio claro y sin ruido
- [ ] Todas las pantallas visibles
- [ ] Transiciones suaves
- [ ] Duración: 9-11 minutos
- [ ] Intro y outro incluidos
- [ ] Música de fondo (sin copyright)
- [ ] Subtítulos (opcional pero recomendado)
- [ ] Exportado en MP4
- [ ] Subido a YouTube/Vimeo
- [ ] Link agregado al README.md del proyecto

---

**Fecha de creación del guión:** Diciembre 2025  
**Versión:** 1.0  
**Proyecto:** Monitor Infantil SIG - INF442-SA
