"""
Comando de Django para sincronizar posiciones GPS desde Traccar Server.

Uso:
    python manage.py sync_traccar                    # Ejecutar una vez
    python manage.py sync_traccar --continuous       # Polling continuo cada 30s
    python manage.py sync_traccar --interval 60      # Polling cada 60 segundos
"""
from django.core.management.base import BaseCommand, CommandError
from apps.gis_tracking.traccar_service import TraccarService, TraccarAPIException
import time
import signal
import sys


class Command(BaseCommand):
    help = 'Sincronizar posiciones GPS desde Traccar Server hacia Django'
    
    def __init__(self):
        super().__init__()
        self.running = True
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=30,
            help='Intervalo de polling en segundos (default: 30)'
        )
        
        parser.add_argument(
            '--continuous',
            action='store_true',
            help='Modo continuo - hacer polling indefinidamente'
        )
        
        parser.add_argument(
            '--once',
            action='store_true',
            help='Ejecutar solo una vez y salir (sin polling continuo)'
        )
    
    def handle(self, *args, **options):
        interval = options['interval']
        continuous = options['continuous']
        run_once = options['once']
        
        # Validar argumentos
        if interval < 5:
            raise CommandError('El intervalo mínimo es 5 segundos')
        
        if continuous and run_once:
            raise CommandError('No se puede usar --continuous y --once simultáneamente')
        
        # Configurar signal handler para Ctrl+C
        def signal_handler(sig, frame):
            self.stdout.write(
                self.style.WARNING('\n🛑 Deteniendo sincronización...')
            )
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Inicializar servicio Traccar
        try:
            traccar = TraccarService()
            self.stdout.write(
                self.style.SUCCESS('🔌 Conectando con Traccar Server...')
            )
            traccar.authenticate()
        except TraccarAPIException as e:
            raise CommandError(f'❌ Error al conectar con Traccar: {e}')
        
        self.stdout.write(
            self.style.SUCCESS('✅ Conexión con Traccar establecida')
        )
        
        # Modo de ejecución
        if run_once or not continuous:
            # Ejecutar una sola vez
            self._sync_once(traccar)
        else:
            # Polling continuo
            self._sync_continuous(traccar, interval)
    
    def _sync_once(self, traccar: TraccarService):
        """Ejecutar sincronización una sola vez"""
        self.stdout.write(
            self.style.SUCCESS('🔄 Sincronizando posiciones...')
        )
        
        try:
            stats = traccar.sync_all_positions()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Sincronización completada:\n'
                    f'  • {stats["synced"]} posiciones nuevas\n'
                    f'  • {stats["skipped"]} sin cambios\n'
                    f'  • {stats["errors"]} errores'
                )
            )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error durante sincronización: {e}')
            )
            raise CommandError(str(e))
    
    def _sync_continuous(self, traccar: TraccarService, interval: int):
        """Polling continuo con intervalo especificado"""
        self.stdout.write(
            self.style.SUCCESS(
                f'🚀 Iniciando sincronización continua (cada {interval}s)\n'
                f'   Presiona Ctrl+C para detener\n'
            )
        )
        
        iteration = 0
        
        while self.running:
            iteration += 1
            
            try:
                self.stdout.write(
                    self.style.HTTP_INFO(
                        f'\n[{iteration}] 🔄 Sincronizando...'
                    )
                )
                
                stats = traccar.sync_all_positions()
                
                if stats['synced'] > 0:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[{iteration}] ✅ {stats["synced"]} nuevas | '
                            f'{stats["skipped"]} sin cambios | '
                            f'{stats["errors"]} errores'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.HTTP_INFO(
                            f'[{iteration}] ⏳ Sin nuevas posiciones'
                        )
                    )
                
                # Esperar hasta el siguiente ciclo
                if self.running:
                    time.sleep(interval)
            
            except KeyboardInterrupt:
                self.stdout.write(
                    self.style.WARNING('\n🛑 Interrupción detectada')
                )
                break
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'[{iteration}] ❌ Error: {e}')
                )
                
                if self.running:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⏳ Reintentando en {interval} segundos...'
                        )
                    )
                    time.sleep(interval)
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Sincronización detenida')
        )
