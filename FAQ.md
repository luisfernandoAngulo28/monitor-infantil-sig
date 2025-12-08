# ❓ Preguntas Frecuentes (FAQ)
## Sistema de Monitoreo Infantil con SIG

**Última actualización:** Diciembre 2025

---

## 📑 Índice de Categorías

1. [Preguntas Generales](#-preguntas-generales)
2. [Para Tutores/Padres](#-para-tutorespadres)
3. [Para Administradores](#-para-administradores)
4. [Técnicas](#-preguntas-técnicas)
5. [Privacidad y Seguridad](#-privacidad-y-seguridad)
6. [Solución de Problemas](#-solución-de-problemas)

---

## 🌟 Preguntas Generales

### ¿Qué es el Sistema de Monitoreo Infantil?

Es una aplicación móvil y web que utiliza tecnología SIG (Sistemas de Información Geográfica) para:
- 📍 Rastrear en tiempo real la ubicación de niños prescolares
- 🔔 Alertar automáticamente a padres/tutores cuando un niño sale del área segura de su kinder
- 🗺️ Visualizar la posición del niño en un mapa
- 📊 Consultar historial de movimientos

### ¿Para qué sirve?

**Objetivos principales:**
1. **Prevenir pérdidas:** Saber siempre dónde está el niño
2. **Detección temprana:** Alertas inmediatas si sale del kinder
3. **Tranquilidad:** Padres pueden ver que el niño está seguro
4. **Respuesta rápida:** Actuar rápido ante incidentes

### ¿Qué dispositivos necesito?

**Para tutores/padres:**
- Smartphone Android 6.0+ o iOS 12+
- Conexión a internet (WiFi o datos móviles)
- Permisos de ubicación activados
- App "Monitor Infantil" instalada

**Para administradores:**
- Computadora con navegador web (Chrome, Firefox, Edge)
- Acceso a internet

### ¿Cuánto cuesta?

**Modelo de licenciamiento:**
- Gratuito para instituciones educativas públicas
- Planes por cantidad de niños para instituciones privadas
- Sin costo para padres/tutores

*(Contactar con el proveedor para detalles específicos)*

### ¿Es obligatorio usar el sistema?

**No.** El uso es voluntario y requiere:
1. Consentimiento informado de los padres
2. Aceptación de términos y condiciones
3. Autorización del centro educativo

Los padres pueden optar por no participar sin penalización.

---

## 👨‍👩‍👧 Para Tutores/Padres

### ¿Cómo me registro en la app?

1. **Contacte al administrador** de su kinder
2. Ellos crearán su cuenta de tutor
3. Recibirá credenciales por email/WhatsApp:
   - Usuario: `maria.lopez`
   - Contraseña temporal: `********`
4. Descargue la app "Monitor Infantil" desde Play Store / App Store
5. Inicie sesión con sus credenciales
6. Cambie su contraseña en el primer acceso

**NOTA:** No puede auto-registrarse. Debe ser dado de alta por el kinder.

### ¿Cómo agrego a mi hijo/a?

**No puede hacerlo directamente.** El administrador del kinder debe:
1. Registrar al niño en el sistema
2. Vincularle como tutor principal o adicional
3. Una vez hecho, verá a su hijo en la app automáticamente

### ¿Qué es el "área segura"?

Es un polígono virtual dibujado sobre el mapa que marca los límites del kinder.

**Incluye:**
- Edificio principal
- Áreas de juego (patios, canchas)
- Zonas de recreo
- Estacionamiento interno

**Cuando el niño está dentro:** ✅ Todo normal  
**Cuando el niño sale:** 🔔 Recibe alerta inmediata

### ¿Cómo sé si mi hijo está en el kinder?

**Opción 1: Abrir la app**
1. Inicie sesión
2. En el dashboard verá:
```
┌────────────────────────────────┐
│ 👦 Carlos López Días           │
│ 🏫 Kinder Arco Iris            │
│ ✅ En área segura              │
│ 🔋 Batería: 85%                │
│ 🕐 Actualizado: Hace 2 min     │
│                                │
│ [Ver en mapa]                  │
└────────────────────────────────┘
```

**Opción 2: Mapa en tiempo real**
1. Toque "Ver en mapa"
2. Verá un pin con la foto de su hijo
3. El polígono del kinder estará marcado en azul

**Opción 3: Notificación automática**
Si el niño sale, recibirá notificación push instantánea.

### ¿Cada cuánto se actualiza la ubicación?

**Frecuencia de actualización:**
- **Tiempo real:** Cada 30 segundos cuando la app está abierta
- **Background:** Cada 5 minutos cuando la app está en segundo plano
- **Sin app:** No se actualiza (debe estar instalada y con permisos)

**IMPORTANTE:** La app debe tener permisos de ubicación "Siempre permitir" para funcionar en background.

### ¿Qué hago si recibo una alerta?

**Pasos a seguir:**

1. **Mantenga la calma** - Puede ser un falso positivo (GPS impreciso)

2. **Revise la alerta:**
```
🔔 ALERTA: Carlos ha salido del área segura
Hora: 14:35:12
Ubicación: Ver en mapa
[Abrir app] [Marcar como leída]
```

3. **Verifique en el mapa:**
   - ¿Realmente está fuera?
   - ¿A cuántos metros del kinder?
   - ¿En qué dirección?

4. **Contacte al kinder:**
   - Llame al número del centro educativo
   - Pregunte si hay alguna actividad externa
   - Confirme que el niño está bien

5. **Si es un incidente real:**
   - Diríjase al kinder inmediatamente
   - Notifique a las autoridades si es necesario
   - Coordine con otros tutores

6. **Marque como resuelta** cuando todo esté bien

### ¿Puedo ver el historial de movimientos?

**Sí.** 

1. Abra la app
2. Seleccione a su hijo
3. Toque "Historial"
4. Verá una línea de tiempo:
```
Historial - Carlos López
┌────────────────────────────────┐
│ 📅 Hoy, 8 de diciembre         │
├────────────────────────────────┤
│ 14:40 ✅ En kinder             │
│ 14:35 🔴 Salió del área        │
│ 14:30 ✅ En kinder             │
│ 12:00 ✅ En kinder             │
│ 08:30 ✅ Llegó al kinder       │
│                                │
│ [Ver en mapa] [Descargar]      │
└────────────────────────────────┘
```

**Retención de datos:** 30 días

### ¿Funciona sin internet?

**No.** El sistema requiere conexión a internet para:
- Enviar posiciones GPS al servidor
- Recibir alertas
- Actualizar el mapa

**Sin internet:**
- Las posiciones se almacenan temporalmente
- Se envían cuando se recupera la conexión
- Las alertas pueden llegar con retraso

### ¿Cuánta batería consume?

**Consumo aproximado:**
- **App abierta:** 5-10% por hora
- **Background (pantalla apagada):** 2-5% por hora
- **Día completo (8 horas):** 15-30%

**Optimización:**
- Usar WiFi en lugar de datos móviles
- Cerrar apps innecesarias
- Activar modo ahorro de batería del dispositivo

**NOTA:** Recibirá alerta si la batería baja del 20%.

### ¿Puedo tener múltiples hijos?

**Sí.** Puede ser tutor de varios niños.

En el dashboard verá:
```
Mis niños
┌────────────────────────────────┐
│ 👦 Carlos López (5 años)       │
│ ✅ En kinder - Batería: 85%    │
├────────────────────────────────┤
│ 👧 Sofía López (4 años)        │
│ ✅ En kinder - Batería: 92%    │
└────────────────────────────────┘
```

Puede alternar entre ellos tocando cada tarjeta.

### ¿Pueden otros tutores ver a mi hijo?

**Solo si están autorizados.**

Hay dos tipos de tutores:
1. **Tutor principal:** Padre/madre (acceso completo)
2. **Tutores adicionales:** Abuelos, tíos, niñera (acceso completo)

**Nadie más** puede ver la ubicación de su hijo.

### ¿Cómo desactivo el monitoreo temporalmente?

**Opción 1: Desde el administrador del kinder**
- Solicite desactivar el tracking
- Se mantienen los datos, pero no se monitorea

**Opción 2: Desinstalar la app**
- Elimine la app del dispositivo del niño
- No se registrarán posiciones

**NOTA:** No puede desactivarlo desde su app de tutor.

---

## 🏫 Para Administradores

### ¿Cómo agrego un nuevo kinder?

Ver **Manual del Administrador**, sección 4.2.

**Resumen:**
1. Admin Django → Centros educativos → Agregar
2. Complete nombre, dirección, código
3. **Crítico:** Defina el polígono del área segura
4. Guarde

**Herramienta recomendada para polígono:** https://geojson.io

### ¿Cómo defino el área segura de un kinder?

**Paso a paso:**

1. Vaya a https://geojson.io
2. Busque la ubicación del kinder en el mapa
3. Use la herramienta de polígono (ícono ⬡)
4. Haga clic en las esquinas del área:
   - Incluya todo el edificio
   - Incluya patios y áreas de juego
   - Agregue ~10 metros de margen
5. Cierre el polígono (último clic = primer punto)
6. En el panel derecho, copie las coordenadas:
```json
{
  "type": "Polygon",
  "coordinates": [[
    [-63.1821, -17.7833],
    [-63.1810, -17.7833],
    ...
  ]]
}
```
7. Convierta a formato WKT:
```
POLYGON((-63.1821 -17.7833, -63.1810 -17.7833, ...))
```
8. Péguelo en el campo "Área segura" del admin

**Herramienta alternativa:** https://arthur-e.github.io/Wicket/sandbox-gmaps3.html

### ¿Cómo registro a un nuevo niño?

**Requisitos previos:**
1. El kinder debe estar registrado
2. Al menos un tutor debe estar creado

**Proceso:**
1. Admin Django → Niños → Agregar
2. Complete datos personales
3. Seleccione centro educativo
4. Seleccione tutor principal
5. Active "Tracking activo"
6. Guarde

**IMPORTANTE:** El `dispositivo_id` se llena automáticamente cuando el tutor abre la app.

### ¿Qué hago si un área segura está mal definida?

**Síntomas:**
- Niños dentro del kinder generan alertas de salida
- Niños fuera no generan alertas

**Solución:**
1. Edite el centro educativo
2. Visualice el polígono actual en geojson.io
3. Identifique el problema:
   - Polígono muy pequeño → Ampliar
   - Polígono mal ubicado → Redibujar
   - Coordenadas invertidas (lat/lng) → Corregir
4. Actualice el polígono
5. Guarde
6. Pruebe con una posición GPS dentro del área

### ¿Cómo gestiono las alertas?

**Ver alertas pendientes:**
1. Admin Django → Alertas
2. Filtro: Estado = "PENDIENTE" o "ENVIADA"
3. Revise cada alerta
4. Si es falsa alarma: Marcar como resuelta
5. Si es real: Coordinar con tutores

**Tipos de alertas:**
- **SALIDA:** Niño fuera del área (revisar inmediatamente)
- **BATERÍA_BAJA:** Dispositivo < 20% (informar a tutor)
- **SIN_SEÑAL:** Sin actualizaciones > 30 min (verificar)

### ¿Cada cuánto debo revisar el sistema?

**Recomendado:**
- **Diario:** Revisar alertas (5 min al inicio del día)
- **Semanal:** Estadísticas y reportes
- **Mensual:** Limpieza de datos antiguos, actualización de áreas

### ¿Cómo exporto datos para reportes?

1. Admin Django → Sección deseada (ej: Alertas)
2. Filtre por período (ej: Última semana)
3. Seleccione registros (marque checkboxes)
4. Acción: "Exportar seleccionados como CSV"
5. Haga clic en "Ir"
6. Descargue el archivo
7. Abra con Excel / Google Sheets

### ¿Cuántos niños puedo monitorear simultáneamente?

**Límites técnicos:**
- Sistema soporta **hasta 1000 niños** simultáneos
- Rendimiento óptimo: 100-200 niños
- Sin límite de centros educativos

**Escalar:** Si necesita más capacidad, contacte soporte técnico.

---

## 🔧 Preguntas Técnicas

### ¿Qué tecnologías usa el sistema?

**Backend:**
- Django 5.0 + GeoDjango
- PostgreSQL 16 + PostGIS 3.4
- Channels 4.0 (WebSocket)
- Redis (pub/sub)

**Frontend:**
- Flutter 3.35.4 (móvil)
- Google Maps SDK
- Firebase Cloud Messaging

**Infraestructura:**
- Servidor: Ubuntu 24.04 LTS
- Web server: Nginx + Daphne
- SSL: Let's Encrypt
- Cloud: DigitalOcean

### ¿Qué es PostGIS?

**PostGIS** es una extensión de PostgreSQL que añade soporte para objetos geográficos.

**Permite:**
- Almacenar geometrías (puntos, polígonos, líneas)
- Realizar consultas espaciales (ej: "¿Está el punto dentro del polígono?")
- Calcular distancias geográficas reales
- Crear índices espaciales para performance

**Ejemplo de query:**
```sql
-- ¿Está el niño dentro del área segura?
SELECT ST_Contains(
  area_kinder,
  posicion_nino
);
```

### ¿Cómo funciona la detección de salida del área?

**Proceso automático:**

1. **Captura GPS:** App móvil obtiene coordenadas cada 30 seg
2. **Envío al servidor:** POST a `/api/posiciones/`
3. **Análisis espacial:** Backend ejecuta:
```python
dentro = kinder.area_segura.contains(posicion.ubicacion)
```
4. **Decisión:**
   - Si `dentro = True` → Todo normal
   - Si `dentro = False` → Generar alerta
5. **Notificación:** Firebase envía push a tutores

**Tecnología:** PostGIS `ST_Contains` (operación punto-en-polígono)

### ¿Qué precisión tiene el GPS?

**Precisión típica:**
- **Exterior (cielo despejado):** 3-10 metros
- **Interior (edificio):** 10-50 metros
- **Con A-GPS (WiFi + GPS):** 1-5 metros

**Factores que afectan:**
- Clima (lluvia, nubes)
- Edificios altos (efecto canyon)
- Interior vs exterior
- Calidad del dispositivo

**Recomendación:** Definir áreas seguras con margen de 10-15 metros.

### ¿Cómo se comunica la app con el servidor?

**Protocolos:**

1. **API REST (HTTP/HTTPS):**
   - Autenticación: JWT tokens
   - Endpoints: `/api/ninos/`, `/api/posiciones/`, etc.
   - Formato: JSON

2. **WebSocket (WSS):**
   - Tiempo real para actualizaciones live
   - Canal: `tracking_{nino_id}`
   - Protocolo: Channels + Daphne

**Ejemplo de flujo:**
```
App → POST /api/token/ → Obtiene JWT
App → POST /api/posiciones/ (con JWT) → Registra posición
Server → Analiza → Si fuera del área → Genera alerta
Server → Firebase → Push notification → Tutores
```

### ¿Los datos están encriptados?

**Sí.**

**En tránsito:**
- HTTPS (TLS 1.3)
- WSS (WebSocket Secure)
- Certificado SSL válido

**En reposo:**
- Base de datos PostgreSQL con contraseñas cifradas (bcrypt)
- Tokens JWT firmados con clave secreta
- Sesiones cifradas

**NO se guarda:**
- Contraseñas en texto plano
- Tokens en cookies sin HTTPS

### ¿Puedo integrar el sistema con otros servicios?

**Sí, via API REST.**

**Endpoints públicos** (requieren autenticación):
- `GET /api/ninos/` - Listar niños
- `GET /api/posiciones/` - Posiciones GPS
- `GET /api/alertas/` - Alertas
- `GET /api/busqueda-cercanos/ninos-cercanos/{lat}/{lng}/` - Búsqueda espacial

**Documentación API:** https://monitor-infantil.duckdns.org/api/docs/

**Casos de uso:**
- Integración con sistema del kinder
- Dashboard personalizado
- Reportes automatizados
- Integración con WhatsApp Business

---

## 🔒 Privacidad y Seguridad

### ¿Quién puede ver la ubicación de mi hijo?

**Solo:**
1. Tutores autorizados (principal + adicionales)
2. Administradores del sistema (personal técnico)
3. Personal del kinder (solo si tienen acceso admin)

**NO pueden ver:**
- Otros padres/tutores
- Público general
- Apps de terceros

### ¿Se venden o comparten los datos?

**NO.** 

**Política de datos:**
- Los datos NO se venden a terceros
- NO se usan para publicidad
- NO se comparten con otras instituciones sin consentimiento
- Solo se usan para el monitoreo de seguridad

**Excepciones legales:**
- Orden judicial
- Investigación policial (con autorización)

### ¿Cuánto tiempo se guardan los datos?

**Retención:**
- **Posiciones GPS:** 30 días
- **Alertas:** 90 días
- **Datos de niños/tutores:** Mientras estén activos
- **Logs del sistema:** 7 días

**Después del período:**
- Datos eliminados automáticamente
- Backups se sobrescriben

**Derecho al olvido:**
Puede solicitar eliminación completa de datos contactando al administrador.

### ¿Qué pasa si me roban el celular?

**Pasos inmediatos:**

1. **Contacte al administrador del kinder**
   - Solicite desactivar el tracking
   - Cambien su contraseña

2. **Cambie su contraseña desde otro dispositivo**
   - Inicie sesión en un navegador web
   - Cambie contraseña

3. **Bloquee el dispositivo remotamente**
   - Android: "Encontrar mi dispositivo"
   - iOS: "Buscar mi iPhone"

4. **Notifique a su operador**
   - Bloquee la línea telefónica
   - Bloquee el IMEI

**El sistema:** No permite acceso sin contraseña. Los datos están protegidos.

### ¿Es seguro para los niños?

**Sí.**

**Medidas de seguridad:**
1. **Ubicación no pública:** Solo tutores autorizados
2. **Sin rastro en redes sociales:** El sistema no publica en redes
3. **Datos encriptados:** HTTPS en todo momento
4. **Sin geolocalización pública:** No aparece en Google Maps

**Privacidad de niños:**
- Cumple con COPPA (Children's Online Privacy Protection Act)
- No recopila datos innecesarios
- Fotos privadas (no públicas)

---

## 🛠️ Solución de Problemas

### No recibo alertas en mi celular

**Causas posibles:**

1. **Notificaciones desactivadas**
   - Android: Ajustes → Apps → Monitor Infantil → Notificaciones → Activar
   - iOS: Ajustes → Notificaciones → Monitor Infantil → Permitir

2. **App cerrada forzosamente**
   - No cierre la app con "Forzar detención"
   - Permita que funcione en segundo plano

3. **Ahorro de batería agresivo**
   - Excluya la app del ahorro de batería
   - Android: Ajustes → Batería → Optimización → Monitor Infantil → No optimizar

4. **Sin conexión a internet**
   - Verifique WiFi o datos móviles

5. **Token Firebase no registrado**
   - Cierre la app completamente
   - Ábrala de nuevo
   - Espere 1-2 minutos

**Solución definitiva:**
1. Desinstale la app
2. Reinicie el dispositivo
3. Reinstale la app
4. Inicie sesión

### La ubicación del niño no se actualiza

**Verificar:**

1. **Permisos de ubicación**
   - Android: Ajustes → Ubicación → Permisos de apps → Monitor Infantil → "Permitir siempre"
   - iOS: Ajustes → Privacidad → Ubicación → Monitor Infantil → "Siempre"

2. **GPS activado**
   - Active el GPS del dispositivo
   - Verifique en modo "Alta precisión"

3. **App abierta**
   - La app debe estar instalada en el dispositivo del niño
   - No necesita estar en primer plano (puede estar en background)

4. **Conexión a internet**
   - Verifique que el dispositivo tenga internet
   - WiFi o datos móviles activos

5. **Batería**
   - Verifique que el dispositivo esté encendido
   - Batería > 5%

**Prueba:**
```
1. Abra la app en el dispositivo del niño
2. Vaya a "Configuración" → "Enviar posición de prueba"
3. Espere 30 segundos
4. Revise en su app de tutor si se actualizó
```

### Recibo alertas falsas (niño está en el kinder pero alerta dice que salió)

**Causa más común:** Área segura muy ajustada o GPS impreciso.

**Soluciones:**

1. **Ampliar el área segura:**
   - Contacte al administrador
   - Solicite agregar 10-15 metros de margen al polígono

2. **Esperar 2-3 actualizaciones:**
   - El GPS a veces tiene error de ~10 metros
   - Si después de 2 minutos sigue dentro, es falsa alarma

3. **Verificar visualmente:**
   - Abra el mapa en la app
   - Vea dónde está realmente el pin del niño
   - Compare con el polígono azul del kinder

4. **Marcar como falsa alarma:**
   - En la alerta, toque "Marcar como resuelta"
   - Agregue nota: "Falsa alarma - GPS impreciso"

### La app se cierra sola

**Causas:**

1. **Memoria insuficiente:**
   - Cierre apps en segundo plano
   - Libere espacio de almacenamiento

2. **Sistema operativo antiguo:**
   - Actualice Android/iOS a la última versión

3. **App desactualizada:**
   - Actualice Monitor Infantil desde la tienda

4. **Conflicto con otra app:**
   - Desinstale apps de "limpieza" o "aceleradores"

**Solución:**
1. Desinstale la app
2. Reinicie el dispositivo
3. Instale la versión más reciente
4. Si persiste, contacte soporte técnico

### "Error 500" en el panel de administración

**Causa:** Error interno del servidor.

**Solución inmediata:**
1. Refresque la página (F5)
2. Cierre sesión y vuelva a iniciar
3. Intente desde otro navegador

**Si persiste:**
- Contacte al equipo técnico
- Proporcione:
  - URL exacta donde ocurrió
  - Hora del error
  - Captura de pantalla

**No intente:**
- Borrar datos manualmente
- Modificar la base de datos
- Ejecutar comandos en el servidor

### El mapa no se muestra en la app

**Verificar:**

1. **Conexión a internet:**
   - Google Maps requiere internet

2. **Permisos de ubicación:**
   - La app necesita acceso a ubicación para centrar el mapa

3. **Google Maps API:**
   - Si el mapa está en gris, puede ser problema de API
   - Contacte al administrador

4. **Caché:**
   - Borre caché de la app:
     - Android: Ajustes → Apps → Monitor Infantil → Almacenamiento → Borrar caché
     - iOS: Desinstale y reinstale

### "Token expirado" al intentar iniciar sesión

**Causa:** Sesión caducada.

**Solución:**
1. Cierre la app completamente
2. Ábrala de nuevo
3. Inicie sesión nuevamente
4. Si el error persiste, verifique:
   - Fecha y hora del dispositivo (debe ser correcta)
   - Conexión a internet estable

### No puedo cambiar mi contraseña

**Desde la app:**
1. Menú → Configuración → Cambiar contraseña
2. Ingrese contraseña actual
3. Ingrese nueva contraseña (2 veces)
4. Guarde

**Desde el navegador:**
1. https://monitor-infantil.duckdns.org/admin/
2. Inicie sesión
3. Superior derecha → Cambiar contraseña

**Olvidé mi contraseña:**
- Contacte al administrador del kinder
- Ellos pueden resetearla

---

## 📞 Contacto y Soporte

### ¿Cómo obtengo ayuda?

**Para tutores/padres:**
1. Contacte al administrador de su kinder
2. Email: admin@kinder-nombre.com
3. Teléfono: Ver datos de contacto del kinder

**Para administradores:**
1. Soporte técnico: soporte@monitor-infantil.com
2. Teléfono: +591 XXX XXX XXX
3. Horario: Lunes a Viernes, 8:00 - 18:00

### ¿Dónde reporto un error o problema técnico?

**Email:** bugs@monitor-infantil.com

**Incluir:**
1. Descripción del problema
2. Pasos para reproducirlo
3. Capturas de pantalla
4. Versión de la app
5. Modelo de dispositivo
6. Sistema operativo (Android X.X / iOS X.X)

### ¿Puedo sugerir nuevas funcionalidades?

**¡Sí!**

**Email:** sugerencias@monitor-infantil.com

**Ideas populares:**
- Geofencing de múltiples áreas (casa, parque, escuela)
- Rutas seguras predefinidas
- Historial de incidentes
- Modo "buscar niño" (si se pierde)
- Integración con wearables (smartwatch)

---

## 📚 Recursos Adicionales

**Documentación:**
- Manual de Usuario: `MANUAL_USUARIO.md`
- Manual de Administrador: `MANUAL_ADMINISTRADOR.md`
- Documentación Técnica: `DOCUMENTACION_TECNICA.md`

**Videos:**
- Tutorial para tutores: (próximamente)
- Tutorial para administradores: (próximamente)

**Comunidad:**
- Grupo de WhatsApp (solicitar acceso)
- Foro de usuarios: (próximamente)

---

**¿Tu pregunta no está aquí?**

Envía tu pregunta a: faq@monitor-infantil.com

La agregaremos en la próxima actualización del FAQ.

---

**Versión del documento:** 1.0  
**Última actualización:** Diciembre 2025  
**Sistema:** Monitor Infantil SIG - INF442-SA
