from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from server.consumers import LogConsumer

websocket_urlpatterns = [
    path('log/', LogConsumer),
]
