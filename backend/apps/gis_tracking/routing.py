"""
Routing de WebSockets para GPS Tracking.

Define las URLs para las conexiones WebSocket.
"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # WebSocket para tracking GPS en tiempo real
    # URL: ws://servidor/ws/tracking/tutor/<tutor_id>/
    re_path(
        r'ws/tracking/tutor/(?P<tutor_id>\d+)/$',
        consumers.GPSTrackingConsumer.as_asgi()
    ),
]
