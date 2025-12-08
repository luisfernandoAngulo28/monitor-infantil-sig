"""
Django settings for Monitor Infantil SIG project.
"""
from pathlib import Path
from decouple import config

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS configuration
# En modo DEBUG, aceptar cualquier host (para desarrollo y Docker)
if DEBUG:
    ALLOWED_HOSTS = ['*']
    # Deshabilitar validación RFC de hostnames en desarrollo
    # Esto permite usar nombres de contenedores Docker con guiones bajos
    import os
    os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
    # Parche para aceptar hosts no-RFC en desarrollo
    from django.http import HttpRequest
    _original_get_host = HttpRequest.get_host
    def _patched_get_host(self):
        try:
            return _original_get_host(self)
        except:
            # En desarrollo, siempre retornar el host sin validación
            return self.META.get('HTTP_HOST', 'localhost')
    HttpRequest.get_host = _patched_get_host
else:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,143.198.30.170').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # GeoDjango
    'django.contrib.gis',
    
    # Third party
    'rest_framework',
    'rest_framework_gis',
    'corsheaders',
    'django_filters',
    'channels',  # WebSocket support
    
    # Local apps
    'apps.core',
    'apps.gis_tracking',
    'apps.alerts',
    'apps.api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ASGI Application (para WebSockets)
ASGI_APPLICATION = 'config.asgi.application'

# Channels configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(config('REDIS_HOST', default='localhost'), config('REDIS_PORT', default=6379, cast=int))],
        },
    },
}

# Database - PostgreSQL with PostGIS (DigitalOcean)
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DATABASE_NAME', default='monitor-infantil-db'),
        'USER': config('DATABASE_USER', default='doadmin'),
        'PASSWORD': config('DATABASE_PASSWORD', default='AVNS_Br2oEVoPiwxrqe4aM29'),
        'HOST': config('DATABASE_HOST', default='monitor-infantil-db-do-user-22120002-0.h.db.ondigitalocean.com'),
        'PORT': config('DATABASE_PORT', default='25060'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es-bo'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'core.Usuario'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Solo para desarrollo
# CORS_ALLOWED_ORIGINS = config(
#     'CORS_ALLOWED_ORIGINS',
#     default='http://localhost:3000,http://127.0.0.1:3000'
# ).split(',')

# Celery Configuration
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# GeoDjango settings
GDAL_LIBRARY_PATH = config('GDAL_LIBRARY_PATH', default=None)
GEOS_LIBRARY_PATH = config('GEOS_LIBRARY_PATH', default=None)
DEFAULT_SRID = 4326  # WGS84 - GPS estándar

# Firebase (Push notifications)
FIREBASE_CREDENTIALS_PATH = config('FIREBASE_CREDENTIALS_PATH', default='')

# Tracking settings
GPS_UPDATE_INTERVAL_SECONDS = 30  # Actualización GPS cada 30 segundos
ALERT_COOLDOWN_MINUTES = 5  # No enviar alertas repetidas en 5 minutos

# Traccar GPS Server Configuration
TRACCAR_SERVER_URL = config('TRACCAR_SERVER_URL', default='http://traccar:8082/api')
TRACCAR_USERNAME = config('TRACCAR_USERNAME', default='admin')
TRACCAR_PASSWORD = config('TRACCAR_PASSWORD', default='admin')
TRACCAR_WEBHOOK_SECRET = config('TRACCAR_WEBHOOK_SECRET', default='change-this-secret-token-in-production')
