from django.urls import re_path
from . import consumers

websocket_urlpatterns = [  # Corrected variable name
    re_path(r'ws/stats/', consumers.StatsConsumer.as_asgi()),
    re_path(r'ws/statsVisual/', consumers.StatsConsumer.as_asgi())

]