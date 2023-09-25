from django.urls import re_path

from chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/send/(?P<user_id>\w+)/$', consumers.ChatConsumer.as_asgi())
]