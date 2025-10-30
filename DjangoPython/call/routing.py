from django.urls import re_path

from . import consumers

call_websockets_urlpatterns = [
    re_path(r'ws/call/', consumers.CallConsumer.as_asgi())
]