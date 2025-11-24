# 🗂️ Guía de Navegación del Proyecto

## 📁 Estructura de Carpetas

```
C:\ProyectoSig\
│
├── 📂 backend/                    # 🔧 Backend Django + GeoDjango
│   ├── apps/                     # Módulos de la aplicación
│   │   ├── core/                # Usuarios, tutores
│   │   ├── gis_tracking/        # Tracking GPS, modelos geoespaciales
│   │   ├── alerts/              # Sistema de alertas
│   │   └── api/                 # API REST
│   ├── config/                   # Configuración Django
│   ├── templates/                # Templates HTML
│   ├── requirements/             # Dependencias Python
│   ├── manage.py
│   ├── docker-compose.yml
│   └── README.md                 # 📖 Documentación del backend
│
├── 📂 web/                        # 🌐 Frontend Web
│   ├── static/                   # CSS, JS, imágenes (futuro)
│   └── README.md                 # 📖 Documentación del frontend
│
├── 📂 mobile/                     # 📱 App Móvil Flutter
│   └── README.md                 # 📖 Guía para crear la app Flutter
│
├── 📂 SIG22/                      # 📚 Documentación del Proyecto
│   ├── docs/                     # Tutoriales y guías
│   │   ├── TUTORIAL.md          # Tutorial completo
│   │   ├── FLUTTER_APP.md       # Guía Flutter con código
│   │   └── QGIS_TUTORIAL.md     # Tutorial QGIS
│   ├── scripts/                  # Scripts útiles
│   │   ├── generate_test_data.py  # Generar datos de prueba
│   │   └── README.md
│   ├── README.md                 # Documentación principal
│   ├── STACK_TECNOLOGICO.md     # Arquitectura del sistema
│   ├── INSTALACION.md           # Guía de instalación
│   └── RESUMEN_PROYECTO.md      # Resumen ejecutivo
│
├── .gitignore
└── README.md                      # 📖 README Principal del Proyecto
```

## 🚀 ¿Por Dónde Empezar?

### 1️⃣ **Primera Vez en el Proyecto**
Leer en orden:
1. `README.md` (raíz) - Descripción general
2. `SIG22/STACK_TECNOLOGICO.md` - Entender la arquitectura
3. `SIG22/INSTALACION.md` - Instalar el backend

### 2️⃣ **Quiero Ejecutar el Backend**
```bash
cd backend
# Ver backend/README.md para instrucciones
```

### 3️⃣ **Quiero Crear la App Móvil**
```bash
cd mobile
# Ver mobile/README.md y SIG22/docs/FLUTTER_APP.md
```

### 4️⃣ **Quiero Aprender a Usar el Sistema**
Leer `SIG22/docs/TUTORIAL.md`

### 5️⃣ **Quiero Digitalizar Áreas con QGIS**
Leer `SIG22/docs/QGIS_TUTORIAL.md`

## 📚 Documentos Clave

| Necesito... | Ver Documento |
|-------------|---------------|
| Descripción del proyecto | `README.md` (raíz) |
| Instalar el sistema | `SIG22/INSTALACION.md` |
| Arquitectura técnica | `SIG22/STACK_TECNOLOGICO.md` |
| Tutorial de uso | `SIG22/docs/TUTORIAL.md` |
| Crear app Flutter | `SIG22/docs/FLUTTER_APP.md` |
| Usar QGIS | `SIG22/docs/QGIS_TUTORIAL.md` |
| Documentación API | `backend/apps/api/API_DOCS.md` |
| Ejecutar backend | `backend/README.md` |
| Ejecutar mobile | `mobile/README.md` |

## 🎯 Flujo de Trabajo Típico

### Desarrollador Backend
```bash
cd backend/
venv\Scripts\activate
python manage.py runserver
# Ver: backend/README.md
```

### Desarrollador Frontend Web
```bash
cd backend/
python manage.py runserver
# Editar: backend/templates/
# Agregar CSS/JS: web/static/
```

### Desarrollador Mobile
```bash
cd mobile/monitor_infantil_app/
flutter run
# Ver: mobile/README.md
# Código base: SIG22/docs/FLUTTER_APP.md
```

### Especialista SIG
```bash
# 1. Digitalizar en QGIS
# Ver: SIG22/docs/QGIS_TUTORIAL.md

# 2. Importar a Django
cd backend/
python manage.py shell
# Ver tutorial en SIG22/docs/QGIS_TUTORIAL.md
```

## 🔧 Scripts Útiles

### Generar Datos de Prueba
```bash
cd backend/
python ../SIG22/scripts/generate_test_data.py
```

## 🆘 Ayuda

¿Necesitas ayuda con...?

- **Instalación**: Ver `SIG22/INSTALACION.md`
- **Backend**: Ver `backend/README.md`
- **Mobile**: Ver `mobile/README.md` y `SIG22/docs/FLUTTER_APP.md`
- **QGIS**: Ver `SIG22/docs/QGIS_TUTORIAL.md`
- **API**: Ver `backend/apps/api/API_DOCS.md`
- **General**: Ver `SIG22/docs/TUTORIAL.md`

## 📝 Notas Importantes

1. **Backend es obligatorio**: El backend Django debe estar ejecutándose para que funcione todo
2. **Mobile es opcional**: Se puede usar solo el panel web
3. **QGIS es para digitalización**: Usar para crear polígonos de kinders
4. **Documentación en SIG22/**: Toda la documentación del proyecto está centralizada aquí

---

**¡Bienvenido al proyecto Monitor Infantil SIG! 🚀**
