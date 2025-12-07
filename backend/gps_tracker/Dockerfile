FROM python:3.12-slim

# Metadata
LABEL maintainer="Monitor Infantil SIG"
LABEL description="GPS Tracker Worker for Chinese GF21 Device"

# Configuración de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY gps_tracker/requirements_tracker.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements_tracker.txt

# Copiar código del tracker
COPY gps_tracker/tracker.py .

# Crear directorio de logs
RUN mkdir -p /var/log && chmod 777 /var/log

# Healthcheck
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Usuario no-root para seguridad
RUN useradd -m -u 1000 tracker && chown -R tracker:tracker /app /var/log
USER tracker

# Comando de inicio
CMD ["python", "-u", "tracker.py"]
