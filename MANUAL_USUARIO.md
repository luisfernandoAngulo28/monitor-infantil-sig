# Manual de Usuario - Monitor Infantil SIG

**Sistema de Monitoreo Infantil con Geolocalización en Tiempo Real**

---

**Versión**: 1.0  
**Fecha**: 6 de diciembre de 2025  
**Proyecto**: Monitor Infantil SIG  
**Materia**: INF442-SA  
**Desarrollador**: Fernando Angulo  
**Servidor**: https://monitor-infantil.duckdns.org

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación de la Aplicación Móvil](#instalación-de-la-aplicación-móvil)
4. [Registro e Inicio de Sesión](#registro-e-inicio-de-sesión)
5. [Pantalla Principal](#pantalla-principal)
6. [Monitoreo en Tiempo Real](#monitoreo-en-tiempo-real)
7. [Gestión de Niños](#gestión-de-niños)
8. [Sistema de Alertas](#sistema-de-alertas)
9. [Áreas Seguras](#áreas-seguras)
10. [Historial de Ubicaciones](#historial-de-ubicaciones)
11. [Configuración](#configuración)
12. [Solución de Problemas](#solución-de-problemas)
13. [Preguntas Frecuentes](#preguntas-frecuentes)
14. [Soporte Técnico](#soporte-técnico)

---

## 1. Introducción

### ¿Qué es Monitor Infantil SIG?

Monitor Infantil SIG es una aplicación móvil que permite a madres, padres y tutores monitorear la ubicación en tiempo real de niños preescolares mediante tecnología GPS y Sistemas de Información Geográfica (SIG).

### ¿Para qué sirve?

- 📍 **Rastreo GPS en Tiempo Real**: Ver la ubicación actual del niño en un mapa
- ⚠️ **Alertas Automáticas**: Recibir notificaciones cuando el niño sale de áreas seguras (Kinder, casa, etc.)
- 🗺️ **Áreas Seguras**: Definir zonas geográficas donde el niño debe permanecer
- 📊 **Historial**: Revisar trayectorias y movimientos pasados
- 🔋 **Monitoreo de Batería**: Control del nivel de batería del dispositivo del niño

### Beneficios

✅ **Seguridad**: Prevención de pérdidas, accidentes o situaciones de riesgo  
✅ **Tranquilidad**: Saber en todo momento dónde está el niño  
✅ **Rapidez**: Respuesta inmediata ante situaciones anormales  
✅ **Automatización**: Sistema que trabaja 24/7 sin intervención manual

---

## 2. Requisitos del Sistema

### Dispositivo del Tutor (Madre/Padre)

**Smartphone con:**
- Android 8.0 (Oreo) o superior
- iOS 12 o superior
- Conexión a Internet (WiFi o datos móviles)
- GPS activado
- Mínimo 100 MB de espacio libre

**Recomendado:**
- Android 10+ o iOS 14+
- 4G/5G para actualizaciones rápidas
- Notificaciones push habilitadas

### Dispositivo del Niño

**Opciones:**
1. **Smartwatch con GPS** (Recomendado)
   - Ejemplo: Xiaomi Mi Watch, Apple Watch, Samsung Galaxy Watch
   - Con conectividad celular o WiFi

2. **Teléfono básico con GPS**
   - Android básico con app instalada
   - Plan de datos prepago

3. **Rastreador GPS dedicado**
   - Dispositivo GPS con SIM card

### Conexión a Internet

- **WiFi** o **datos móviles** activos en ambos dispositivos
- Velocidad mínima: 512 Kbps (suficiente para enviar coordenadas GPS)

---

## 3. Instalación de la Aplicación Móvil

### Android

#### Opción A: Google Play Store (Cuando esté publicada)

1. Abre **Google Play Store**
2. Busca "Monitor Infantil SIG"
3. Toca **Instalar**
4. Espera a que descargue e instale
5. Toca **Abrir**

#### Opción B: APK Directo (Versión de prueba)

1. Descarga el archivo `monitor-infantil.apk` desde el enlace proporcionado
2. Ve a **Configuración** → **Seguridad**
3. Activa **"Permitir instalación de aplicaciones de origen desconocido"**
4. Abre el archivo `.apk` descargado
5. Toca **Instalar**
6. Toca **Abrir** cuando finalice

### iOS

#### App Store (Cuando esté publicada)

1. Abre **App Store**
2. Busca "Monitor Infantil SIG"
3. Toca **Obtener**
4. Ingresa tu contraseña de Apple ID si se solicita
5. Toca **Abrir**

### Permisos Necesarios

Al abrir la app por primera vez, solicitará los siguientes permisos:

- ✅ **Ubicación**: Requerido para mostrar tu posición y la del niño
- ✅ **Notificaciones**: Para recibir alertas de seguridad
- 📷 **Cámara** (opcional): Para tomar fotos de perfil
- 📁 **Almacenamiento** (opcional): Para guardar historial offline

**⚠️ Importante**: Debes aceptar todos los permisos para que la app funcione correctamente.

---

## 4. Registro e Inicio de Sesión

### Primer Uso: Registro

1. **Abre la aplicación**
2. Toca **"Registrarse"** o **"Crear cuenta"**
3. Completa el formulario:

   ```
   📧 Email: tuCorreo@ejemplo.com
   🔑 Contraseña: (mínimo 8 caracteres)
   🔑 Confirmar contraseña: (repetir)
   👤 Nombre: María
   👤 Apellidos: González López
   📞 Teléfono: +591 70123456
   👨‍👩‍👧 Relación: Madre / Padre / Tutor / Otro
   🆔 CI/DNI: 1234567 (opcional)
   ```

4. Toca **"Registrarse"**
5. Espera el mensaje: **"Cuenta creada exitosamente"**
6. Serás redirigido al inicio de sesión

### Iniciar Sesión

1. Ingresa tu **email** y **contraseña**
2. Toca **"Iniciar sesión"**
3. Serás redirigido a la **pantalla principal**

### Recuperar Contraseña

Si olvidaste tu contraseña:

1. Toca **"¿Olvidaste tu contraseña?"**
2. Ingresa tu email
3. Recibirás un correo con instrucciones
4. Sigue el enlace y crea una nueva contraseña

---

## 5. Pantalla Principal

Al iniciar sesión verás la **pantalla principal** con:

### Elementos de la Interfaz

```
┌─────────────────────────────────┐
│  👤 Perfil    🔔 Alertas    ⚙️   │
├─────────────────────────────────┤
│                                 │
│         🗺️ MAPA                 │
│      (Vista principal)          │
│                                 │
│   📍 Niños en el mapa           │
│   🟢 Verde = En área segura     │
│   🔴 Rojo = Fuera del área      │
│                                 │
├─────────────────────────────────┤
│  👶 Mis Niños                   │
│  ├─ Juan (8 años) 🟢           │
│  └─ María (6 años) 🟢          │
├─────────────────────────────────┤
│  [Ver Historial] [Configurar]   │
└─────────────────────────────────┘
```

### Barra Superior

- **👤 Perfil**: Ver y editar tu información personal
- **🔔 Alertas**: Notificaciones recientes (número rojo indica alertas sin leer)
- **⚙️ Configuración**: Ajustes de la aplicación

### Indicador de Conexión

En la esquina superior derecha verás:

- **🟢 En línea**: Conexión activa con el servidor
- **🔴 Desconectado**: Sin conexión (verifica tu internet)

---

## 6. Monitoreo en Tiempo Real

### Ver Ubicación del Niño

1. En la pantalla principal, verás el **mapa** con marcadores de tus niños
2. Cada niño aparece con un **pin de color**:
   - 🟢 **Verde**: El niño está **dentro** del área segura
   - 🔴 **Rojo**: El niño está **fuera** del área segura (¡ALERTA!)

### Información del Marcador

Toca un **marcador** en el mapa para ver:

```
┌─────────────────────────┐
│ 👶 Juan Pérez López     │
├─────────────────────────┤
│ 📍 Ubicación:           │
│    -17.7833, -63.1812   │
│                         │
│ ✅ Estado:              │
│    En área segura       │
│                         │
│ 🔋 Batería: 85%         │
│                         │
│ 🕐 Actualización:       │
│    Hace 10 segundos     │
│                         │
│ [Ver más detalles]      │
└─────────────────────────┘
```

### Centrar Mapa

- Toca el botón **🎯** (ubicación) en la esquina inferior derecha
- El mapa se centrará en el primer niño de tu lista

### Zoom del Mapa

- **Pellizca** con dos dedos para hacer zoom in/out
- **Doble toque** para acercarte rápidamente

---

## 7. Gestión de Niños

### Ver Lista de Niños

1. Desde el menú principal, toca **"Mis Niños"**
2. Verás la lista de niños que tienes registrados:

```
┌─────────────────────────────────┐
│  👶 Mis Niños (2)               │
├─────────────────────────────────┤
│  👦 Juan Pérez López            │
│  📅 8 años                      │
│  🏫 Kinder Los Pitufos          │
│  📍 Estado: 🟢 En área segura   │
│  🔋 Batería: 85%                │
│  [Ver en mapa] [Detalles]       │
├─────────────────────────────────┤
│  👧 María González              │
│  📅 6 años                      │
│  🏫 Rayito de Sol               │
│  📍 Estado: 🟢 En área segura   │
│  🔋 Batería: 92%                │
│  [Ver en mapa] [Detalles]       │
└─────────────────────────────────┘
```

### Agregar un Niño

1. Toca el botón **"+"** o **"Agregar niño"**
2. Completa el formulario:

   ```
   📝 Nombre: Juan
   📝 Apellido Paterno: Pérez
   📝 Apellido Materno: López (opcional)
   📅 Fecha de Nacimiento: 15/03/2018
   🚻 Sexo: Masculino / Femenino
   📸 Foto: [Tomar foto] [Galería] (opcional)
   🏫 Centro Educativo: Seleccionar...
   📱 ID Dispositivo: 123456789 (código del GPS/smartwatch)
   ✅ Tracking Activo: Sí/No
   ```

3. Toca **"Guardar"**

### Editar Información del Niño

1. En la lista de niños, toca **"Detalles"**
2. Toca el ícono de **lápiz** ✏️
3. Modifica los datos necesarios
4. Toca **"Guardar cambios"**

### Desactivar Tracking

Si temporalmente no quieres monitorear a un niño:

1. Entra a **Detalles** del niño
2. Desactiva el switch **"Tracking Activo"**
3. El niño seguirá registrado pero no aparecerá en el mapa

---

## 8. Sistema de Alertas

### Tipos de Alertas

#### 🔴 Alerta de Salida de Área

**¿Cuándo se genera?**
- Cuando el niño sale del área segura definida (ej: polígono del kinder)

**¿Qué recibes?**
- ⚠️ Notificación push en tu celular
- 📱 Alerta en la app con sonido
- 📧 Email (si está configurado)

**Ejemplo de notificación:**
```
⚠️ ALERTA DE SEGURIDAD

Juan Pérez López ha salido del área segura

🏫 Kinder: Los Pitufos
📍 Ubicación actual: -17.7900, -63.1900
🕐 Hora: 10:35 AM
🔋 Batería: 65%

[Ver en mapa] [Contactar centro]
```

#### 🟡 Alerta de Batería Baja

**¿Cuándo se genera?**
- Cuando la batería del dispositivo del niño está por debajo del 20%

**Mensaje:**
```
🔋 Batería Baja

El dispositivo de Juan tiene 15% de batería

⚠️ Recargue pronto para no perder el rastreo
```

### Ver Alertas

1. Toca el ícono **🔔** en la barra superior
2. Verás la lista de alertas:

```
┌─────────────────────────────────┐
│  🔔 Alertas (3)                 │
├─────────────────────────────────┤
│  🔴 NUEVA - Hace 5 min          │
│  Juan salió del área segura     │
│  Kinder Los Pitufos             │
│  [Ver ubicación]                │
├─────────────────────────────────┤
│  🟡 Hace 1 hora                 │
│  Batería baja - María (18%)     │
│  [Marcar como leída]            │
├─────────────────────────────────┤
│  ✅ RESUELTA - Hace 2 horas     │
│  Juan volvió al área segura     │
│  [Ver detalles]                 │
└─────────────────────────────────┘
```

### Responder a una Alerta

Cuando recibes una alerta de salida de área:

1. **VER UBICACIÓN**:
   - Toca la alerta
   - Se abrirá el mapa mostrando dónde está el niño

2. **CONTACTAR AL CENTRO EDUCATIVO**:
   - Llama al teléfono del kinder (aparece en la alerta)

3. **MARCAR COMO LEÍDA**:
   - Toca **"Marcar como leída"** cuando hayas revisado

4. **RESOLVER ALERTA**:
   - Cuando el niño regrese al área segura, la alerta se marcará automáticamente como **"Resuelta"**

---

## 9. Áreas Seguras

### ¿Qué son las Áreas Seguras?

Son **polígonos geográficos** que definen zonas donde el niño debe permanecer. Por ejemplo:
- 🏫 Centro educativo (Kinder)
- 🏠 Casa
- 🏞️ Parque
- 👵 Casa de los abuelos

### Ver Áreas Seguras

1. En el mapa, las áreas seguras aparecen como **zonas sombreadas**
2. Diferentes colores indican diferentes tipos de áreas

### Crear Área Segura (Función Administrativa)

**Nota**: Esta función está disponible solo para administradores en el panel web.

**Para administradores:**
1. Accede a: https://monitor-infantil.duckdns.org/admin/
2. Ve a **Centros Educativos** → **Añadir**
3. Completa los datos y dibuja el polígono en el mapa
4. Guarda

### Margen de Tolerancia

Cada área segura tiene un **margen de tolerancia** (ej: 15 metros). Esto significa:
- Si el niño está a 10 metros fuera del polígono, **NO se genera alerta**
- Si está a 20 metros fuera, **SÍ se genera alerta**

Esto evita **falsas alarmas** por imprecisiones del GPS.

---

## 10. Historial de Ubicaciones

### Acceder al Historial

1. Selecciona un niño de tu lista
2. Toca **"Ver historial"**
3. Selecciona el período de tiempo:
   - Último día
   - Última semana
   - Último mes
   - Personalizado (selecciona fechas)

### Visualización del Historial

```
┌─────────────────────────────────┐
│  📊 Historial - Juan Pérez      │
│  📅 6 de diciembre 2025         │
├─────────────────────────────────┤
│  🗺️ Mapa con trayectoria        │
│  (línea que conecta puntos GPS) │
│                                 │
│  ─── Ruta del niño ───          │
│                                 │
├─────────────────────────────────┤
│  📋 Lista de ubicaciones:       │
│                                 │
│  10:35 AM - En Kinder 🟢        │
│  📍 -17.7750, -63.1810          │
│                                 │
│  09:15 AM - Llegó al Kinder 🟢  │
│  📍 -17.7752, -63.1812          │
│                                 │
│  08:30 AM - Salió de casa 🏠    │
│  📍 -17.7800, -63.1850          │
└─────────────────────────────────┘
```

### Exportar Historial

1. En la pantalla de historial, toca **⋮** (menú)
2. Selecciona **"Exportar"**
3. Elige formato:
   - PDF (reporte)
   - CSV (datos)
   - KML (para Google Earth)

---

## 11. Configuración

### Acceder a Configuración

Toca el ícono **⚙️** en la barra superior.

### Opciones Disponibles

#### 🔔 Notificaciones

```
✅ Alertas de salida de área
✅ Alertas de batería baja
✅ Sonido de notificación
✅ Vibración
□ Modo No Molestar (horarios)
```

#### 🗺️ Mapa

```
Tipo de mapa:
○ Estándar (por defecto)
○ Satélite
○ Terreno
○ Híbrido

Zoom automático: ✅
Mostrar mi ubicación: ✅
```

#### ⏱️ Actualizaciones GPS

```
Frecuencia de actualización:
○ 10 segundos (consume más batería)
○ 30 segundos (recomendado)
○ 1 minuto (ahorra batería)
```

#### 🔐 Seguridad

```
✅ Requerir contraseña al abrir
□ Huella digital / Face ID
□ Bloqueo automático (5 min)
```

#### 📞 Contactos de Emergencia

Agrega números de teléfono para llamar rápidamente:

```
+ Agregar contacto
  └─ Policía: 110
  └─ Kinder: 3-3334455
  └─ Papá: 70999888
```

---

## 12. Solución de Problemas

### Problema 1: No veo la ubicación del niño

**Posibles causas y soluciones:**

✅ **Verifica conexión a Internet**
   - Asegúrate de tener WiFi o datos móviles activos
   - Prueba abrir un navegador web

✅ **Verifica permisos de ubicación**
   - Ve a Configuración del teléfono → Aplicaciones → Monitor Infantil
   - Permisos → Ubicación → **"Permitir todo el tiempo"**

✅ **Verifica que el dispositivo del niño esté encendido**
   - El smartwatch o GPS debe estar activo
   - Debe tener batería suficiente

✅ **Verifica el indicador de conexión**
   - Si dice "Desconectado", cierra y abre la app

### Problema 2: No recibo alertas

**Soluciones:**

✅ **Verifica permisos de notificaciones**
   - Configuración → Aplicaciones → Monitor Infantil → Notificaciones → **Activadas**

✅ **Verifica configuración en la app**
   - Configuración → Notificaciones → **Alertas activadas**

✅ **Verifica que el niño tenga tracking activo**
   - Mis Niños → Detalles del niño → **Tracking Activo: Sí**

### Problema 3: La app se cierra sola

**Soluciones:**

✅ **Actualiza la aplicación**
   - Ve a Play Store y busca actualizaciones

✅ **Borra caché de la app**
   - Configuración → Aplicaciones → Monitor Infantil → Almacenamiento → **Borrar caché**

✅ **Reinstala la app**
   - Desinstala y vuelve a instalar (tus datos se mantendrán en el servidor)

### Problema 4: El mapa no carga

**Soluciones:**

✅ **Verifica conexión a Internet**

✅ **Verifica permisos de ubicación**

✅ **Reinicia la app**
   - Cierra completamente y vuelve a abrir

✅ **Borra datos de la app** (último recurso)
   - Configuración → Aplicaciones → Monitor Infantil → Almacenamiento → **Borrar datos**
   - Tendrás que iniciar sesión nuevamente

### Problema 5: GPS impreciso

**Causas comunes:**

- 📡 Mala señal GPS (dentro de edificios)
- 🌧️ Clima adverso
- 🏢 Zonas urbanas densas con edificios altos

**Soluciones:**

✅ Espera unos segundos a que el GPS se estabilice
✅ Asegúrate de estar en un lugar con cielo despejado
✅ Verifica que el GPS del dispositivo esté activado

---

## 13. Preguntas Frecuentes

### ¿Cuántos niños puedo monitorear?

No hay límite. Puedes agregar tantos niños como necesites.

### ¿Funciona sin Internet?

No. La app requiere conexión a Internet para enviar/recibir ubicaciones en tiempo real.

### ¿Cuánto consume de batería?

Con actualizaciones cada 30 segundos, consume aproximadamente:
- **Tutor**: 5-10% más de batería por hora
- **Niño** (dispositivo GPS): 15-20% por hora

### ¿Es segura mi información?

Sí. Todos los datos están:
- 🔒 Encriptados con HTTPS/SSL
- 🔐 Protegidos con autenticación
- 🛡️ Almacenados en servidores seguros

### ¿Puedo tener varios tutores por niño?

Sí. Un niño puede tener un **tutor principal** y **tutores adicionales** (papá, mamá, abuelos, etc.). Todos recibirán las alertas.

### ¿Qué pasa si el niño apaga el GPS?

- Se dejará de recibir actualizaciones
- La última ubicación conocida permanecerá visible
- Recibirás una alerta de **"Sin señal GPS"**

### ¿Funciona fuera de Bolivia?

Sí. El sistema funciona en cualquier lugar del mundo que tenga cobertura GPS e Internet.

### ¿Cuánto cuesta?

**Versión académica**: Gratuita para pruebas del proyecto universitario.

---

## 14. Soporte Técnico

### Contacto

**Email**: fernando.fa671@gmail.com  
**Teléfono**: [Tu número]  
**Horario**: Lunes a Viernes, 9:00 AM - 6:00 PM

### Recursos Adicionales

- 📖 **Documentación técnica**: [PROYECTO_RESUMEN.md](https://github.com/luisfernandoAngulo28/monitor-infantil-sig)
- 🌐 **Panel administrativo**: https://monitor-infantil.duckdns.org/admin/
- 🐛 **Reportar errores**: Crea un issue en GitHub

### Actualizaciones

La aplicación se actualiza automáticamente cuando:
- Hay nuevas funcionalidades
- Se corrigen errores
- Se mejora el rendimiento

Recibirás una notificación cuando haya actualizaciones disponibles.

---

## Glosario de Términos

- **GPS**: Sistema de Posicionamiento Global (satélites que detectan ubicación)
- **SIG**: Sistema de Información Geográfica (análisis espacial con mapas)
- **Área Segura**: Zona geográfica donde el niño debe permanecer
- **Polígono**: Forma geométrica cerrada que delimita un área en el mapa
- **Tracking**: Rastreo o seguimiento de la ubicación
- **WebSocket**: Tecnología para comunicación en tiempo real
- **SSL/HTTPS**: Protocolo de seguridad para encriptar datos

---

## Capturas de Pantalla

*(Para la versión PDF, incluir capturas de pantalla aquí)*

1. **Pantalla de Login**
2. **Mapa Principal con marcadores**
3. **Detalle de niño**
4. **Lista de alertas**
5. **Configuración**
6. **Historial de ubicaciones**

---

## Notas Finales

### Recomendaciones de Uso

✅ **Mantén la app actualizada** siempre a la última versión  
✅ **Verifica permisos** después de actualizaciones del sistema operativo  
✅ **Carga el dispositivo del niño** cada noche  
✅ **Revisa alertas** al menos 2-3 veces al día  
✅ **Prueba el sistema** antes del primer día de clases  

### Privacidad

- Solo **tú** (y otros tutores autorizados) pueden ver la ubicación del niño
- Los datos **no se comparten** con terceros
- Puedes **eliminar tu cuenta** en cualquier momento desde Configuración

### Limitaciones

- Requiere que el dispositivo del niño tenga GPS y conectividad
- La precisión del GPS puede variar (±5-15 metros)
- En interiores la señal GPS puede ser débil

---

**© 2025 Monitor Infantil SIG - Proyecto Académico INF442-SA**  
**Universidad**: [Tu Universidad]  
**Docente**: Ing. Franklin Calderón Flores
