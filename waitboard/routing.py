# waiting/routing.py
from django.urls import re_path
from .consumers import WaitingListConsumer

websocket_urlpatterns = [
    re_path(r"ws/wait_list/$", WaitingListConsumer.as_asgi()),
    
]