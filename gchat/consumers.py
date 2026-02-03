import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from  .models import ChatRoom as chatroom, Message as gmessage   

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'gchat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_email = text_data_json['sender_email']
        room_name = text_data_json['room_name']

        room_id =async_to_sync(self.get_or_create_room)(room_name)
        async_to_sync(self.save_message)(room_id, sender_email, message)

        

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'gchat_message',
                'message': message,
                'sender_email': sender_email,
                'room_name': room_name
            }
        )

    # Receive message from room group
    def gchat_message(self, event):
        message = event['message']
        sender_email = event['sender_email']
        room_name = event['room_name']
        # Send message to WebSocket     
        self.send(text_data=json.dumps({
            'message': message,
            'sender_email': sender_email,        
            'room_name': room_name
        }))

    @database_sync_to_async
    def get_or_create_room(self, room_name):
        sql = "select id,name from gchat_chatroom where name = %s"
        row = chatroom.objects.raw(sql, [room_name])
        if not row:
            chatroom.objects.create(name=room_name)
            return self.get_or_create_room(room_name)
        else:
            return row[0].id
       


    @database_sync_to_async
    def save_message(self, room_id, sender_email, message):
        gmessage.objects.create(room_id=room_id, sender_email=sender_email, text=message)
       