# 🔧 Backend - Monitor Infantil SIG

API REST desarrollada con Django + GeoDjango para monitoreo geoespacial de niños.

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.11+
- PostgreSQL 15 + PostGIS 3.4
- Docker (opcional)

### Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Instalar dependencias
pip install -r requirements/dev.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 4. Levantar base de datos (con Docker)
docker-compose up -d db

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Ejecutar servidor
python manage.py runserver
```

## 📡 Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/token/` | Login (JWT) |
| GET | `/api/ninos/` | Listar niños |
| POST | `/api/ninos/{id}/registrar_posicion/` | Enviar GPS |
| GET | `/api/ninos/{id}/estado/` | Estado actual |
| GET | `/api/mis-alertas/` | Alertas del tutor |

Ver documentación completa: `apps/api/API_DOCS.md`

## 🗄️ Base de Datos

### Con Docker (Recomendado)
```bash
docker-compose up -d
```

### Manual
```sql
CREATE DATABASE monitor_infantil_db;
\c monitor_infantil_db
CREATE EXTENSION postgis;
```

## 🧪 Tests

```bash
python manage.py test apps.api.tests
```

## 📚 Estructura

```
backend/
├── apps/
│   ├── core/           # Usuarios, tutores
│   ├── gis_tracking/   # Modelos geoespaciales
│   ├── alerts/         # Sistema de alertas
│   └── api/            # API REST
├── config/             # Configuración Django
├── templates/          # Templates web
├── requirements/       # Dependencias
├── manage.py
└── docker-compose.yml
```

## 🔐 Configuración

Variables importantes en `.env`:
```
SECRET_KEY=tu-secret-key
DEBUG=True
DATABASE_NAME=monitor_infantil_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres123
FIREBASE_CREDENTIALS_PATH=path/to/firebase.json
```

## 🌐 URLs

- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/
- **Dashboard**: http://localhost:8000/

## 📖 Documentación

Ver carpeta `../SIG22/docs/` para tutoriales completos.
