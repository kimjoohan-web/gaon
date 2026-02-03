from django.urls import path
from . import views

pp_name = 'chat'
urlpatterns =[
    path('', views.chat_index, name='chat_index'),
    path('rooms/', views.ChatRoomListCreateView.as_view(), name='chat_rooms'),
    path('<int:room_id>/messages', views.MessageListView.as_view(), name='chat_messages'),   
]