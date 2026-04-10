# waiting/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Waitboard

class WaitingListConsumer(AsyncWebsocketConsumer):
    group_name = "wait_list"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_waiting_list()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "add":
            name = data.get("name", "").strip()
            phone = data.get("phone", "").strip()

            if name and phone:
                await self.create_waiting_user(name, phone)
                await self.broadcast_waiting_list()

        elif action == "delete":
            waiter_id = data.get("w_id")
            if waiter_id:
                await self.delete_waiting_user(waiter_id)
                await self.broadcast_waiting_list()

    async def send_waiting_list(self):
        waiters = await self.get_waiting_users()
        await self.send(text_data=json.dumps({
            "type": "wait_list",
            "waiters": waiters
        }))

    async def broadcast_waiting_list(self):
        waiters = await self.get_waiting_users()
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "wait_list_message",
                "waiters": waiters
            }
        )

    async def wait_list_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "wait_list",
            "waiters": event["waiters"]
        }))

    @sync_to_async
    def create_waiting_user(self, name, phone):
        Waitboard.objects.create(w_name=name, w_hp=phone)

    @sync_to_async
    def delete_waiting_user(self, waiter_id):
        Waitboard.objects.filter(w_id=waiter_id).delete()

    @sync_to_async
    def get_waiting_users(self):
        users = Waitboard.objects.all()
        return [
            {
                "w_id": user.w_id,
                "name": user.w_name,
                "phone": user.w_hp,     
                "created_at": user.w_created_at.isoformat(),
                "w_YN": user.w_YN
            }
            for user in users
        ]
