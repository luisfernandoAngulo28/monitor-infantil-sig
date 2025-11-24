# 🌐 Frontend Web - Monitor Infantil SIG

Panel web de administración y monitoreo construido con Django Templates y Leaflet.js

## 📋 Descripción

El frontend web permite:
- 📊 Dashboard con estadísticas en tiempo real
- 🗺️ Mapa interactivo con Leaflet.js
- 👥 Gestión de centros educativos, niños y tutores
- ⚠️ Visualización de alertas

## 🚀 Ejecutar

El frontend web está integrado en el backend Django. Para ejecutarlo:

```bash
cd ../backend
python manage.py runserver
```

Luego abrir: http://localhost:8000/

## 🗂️ Estructura

```
web/
├── static/          # CSS, JS, imágenes (futuro)
│   ├── css/
│   ├── js/
│   └── img/
└── README.md
```

**Nota**: Los templates HTML están en `../backend/templates/`

## 🎨 Tecnologías

- **Framework**: Django Templates
- **Mapas**: Leaflet.js + OpenStreetMap
- **UI**: Bootstrap 5
- **Charts**: (Opcional) Chart.js para gráficos

## 📱 Pantallas

### Dashboard (`/`)
- Estadísticas: total niños, dentro del área, alertas activas
- Alertas recientes
- Acciones rápidas

### Mapa en Tiempo Real (`/mapa/`)
- Polígonos de áreas seguras (azul)
- Marcadores GPS de niños (verde/rojo)
- Lista lateral de niños monitoreados
- Auto-refresh cada 30 segundos

### Panel Admin (`/admin/`)
- CRUD completo de todas las entidades
- Editor de mapas GIS integrado
- Gestión de usuarios y permisos

## 🔧 Personalización

### Cambiar Estilo
Editar archivos en `static/css/` (cuando se creen)

### Agregar Componentes
Ver `../backend/templates/` para editar templates

## 🌐 Despliegue

Para producción, configurar:
```bash
# En backend/.env
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com

# Recolectar archivos estáticos
cd ../backend
python manage.py collectstatic
```

## 📖 Documentación

- [Tutorial completo](../SIG22/docs/TUTORIAL.md)
- [Stack tecnológico](../SIG22/STACK_TECNOLOGICO.md)
