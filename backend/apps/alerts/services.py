"""
Servicios para envío de notificaciones push
"""
from django.conf import settings
from .models import NotificacionTutor


class NotificacionService:
    """
    Servicio para enviar notificaciones push usando Firebase Cloud Messaging
    """
    
    @staticmethod
    def enviar_push_notification(tutor, alerta):
        """
        Envía una notificación push al tutor
        
        Args:
            tutor: Instancia de Tutor
            alerta: Instancia de Alerta
        
        Returns:
            NotificacionTutor creada
        """
        notificacion = NotificacionTutor.objects.create(
            alerta=alerta,
            tutor=tutor
        )
        
        # Verificar si el tutor tiene firebase_token
        if not tutor.usuario.firebase_token:
            notificacion.enviada_exitosamente = False
            notificacion.error_mensaje = "Tutor no tiene token FCM configurado"
            notificacion.save()
            return notificacion
        
        # Verificar si las notificaciones están activas
        if not tutor.usuario.notificaciones_activas:
            notificacion.enviada_exitosamente = False
            notificacion.error_mensaje = "Notificaciones desactivadas por el usuario"
            notificacion.save()
            return notificacion
        
        try:
            # Enviar usando Firebase Admin SDK
            mensaje_id = NotificacionService._enviar_fcm(
                token=tutor.usuario.firebase_token,
                titulo=f"⚠️ Alerta: {alerta.get_tipo_alerta_display()}",
                cuerpo=alerta.mensaje,
                datos={
                    'alerta_id': str(alerta.id),
                    'nino_id': str(alerta.nino.id),
                    'tipo': alerta.tipo_alerta,
                    'latitud': str(alerta.posicion_gps.ubicacion.y) if alerta.posicion_gps else None,
                    'longitud': str(alerta.posicion_gps.ubicacion.x) if alerta.posicion_gps else None,
                }
            )
            
            notificacion.enviada_exitosamente = True
            notificacion.mensaje_id = mensaje_id
            
        except Exception as e:
            notificacion.enviada_exitosamente = False
            notificacion.error_mensaje = str(e)
        
        notificacion.save()
        return notificacion
    
    @staticmethod
    def _enviar_fcm(token, titulo, cuerpo, datos=None):
        """
        Envía mensaje usando Firebase Cloud Messaging
        
        Para implementar en producción:
        - Configurar firebase-admin
        - Obtener credenciales de Firebase
        """
        # TODO: Implementar con firebase-admin
        # Por ahora, simulación
        
        if not settings.FIREBASE_CREDENTIALS_PATH:
            raise Exception("Firebase no configurado")
        
        # Simulación de envío
        print(f"[PUSH NOTIFICATION] {titulo}: {cuerpo}")
        print(f"Token: {token}")
        print(f"Datos: {datos}")
        
        # En producción:
        # import firebase_admin
        # from firebase_admin import messaging
        # 
        # message = messaging.Message(
        #     notification=messaging.Notification(
        #         title=titulo,
        #         body=cuerpo,
        #     ),
        #     data=datos or {},
        #     token=token,
        # )
        # 
        # response = messaging.send(message)
        # return response
        
        return f"simulated_msg_id_{token[:10]}"
    
    @staticmethod
    def enviar_notificacion_multiple(tutores, titulo, mensaje, datos=None):
        """
        Envía notificación a múltiples tutores
        """
        resultados = []
        for tutor in tutores:
            # Crear alerta manual
            from apps.alerts.models import Alerta
            alerta = Alerta.objects.create(
                nino=tutor.ninos_principal.first(),  # Primer niño del tutor
                tipo_alerta='MANUAL',
                mensaje=mensaje
            )
            
            resultado = NotificacionService.enviar_push_notification(tutor, alerta)
            resultados.append(resultado)
        
        return resultados
