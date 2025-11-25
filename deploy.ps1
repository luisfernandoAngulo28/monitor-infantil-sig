# Script para desplegar cambios al servidor DigitalOcean
param(
    [string]$Message = "Actualización automática"
)

Write-Host "🚀 Iniciando despliegue..." -ForegroundColor Cyan

# 1. Commit y push local
Write-Host "`n📝 Guardando cambios locales..." -ForegroundColor Yellow
git add .
git commit -m $Message
git push

# 2. Actualizar en servidor
Write-Host "`n☁️  Actualizando servidor DigitalOcean..." -ForegroundColor Yellow
ssh root@143.198.30.170 @"
cd /opt/monitor-infantil-sig
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt --quiet
python manage_simple.py migrate
pkill -f 'python.*manage_simple.py' || true
nohup python manage_simple.py runserver 0.0.0.0:8000 > /var/log/django.log 2>&1 &
sleep 2
echo '✅ Servidor actualizado y reiniciado'
"@

Write-Host "`n✅ Despliegue completado!" -ForegroundColor Green
Write-Host "🌐 Servidor: http://143.198.30.170:8000" -ForegroundColor Cyan
