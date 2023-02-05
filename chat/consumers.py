''' Django Channels consumers '''
import json

from django.contrib.auth import get_user_model

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    ''' Consumer to handle websocket connections for the chat '''
    sender = None
    receiver = None

    async def connect(self):
        self.sender = self.scope['user']
        self.receiver = await database_sync_to_async(self.get_superuser)()

        if not self.sender.is_authenticated:
            await self.close()
            return

        await self.accept()

        await self.channel_layer.group_add(
            f"chat-{self.sender.id}-{self.receiver.id}",
            self.channel_name)

        await self.channel_layer.group_add(
            f"chat-{self.receiver.id}-{self.sender.id}",
            self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            f"chat-{self.sender.id}-{self.receiver.id}",
            self.channel_name)
        await self.channel_layer.group_discard(
            f"chat-{self.receiver.id}-{self.sender.id}",
            self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await database_sync_to_async(self.new_message)(message=message)

        await self.channel_layer.group_send(
            f"chat-{self.sender.id}-{self.receiver.id}",
            {
                "type": "chat_message",
                "message": message,
                "sender": self.sender.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    def get_superuser(self):
        return get_user_model().objects.filter(
            is_superuser=True).first()

    def new_message(self, message):
        ChatMessage.objects.create(
            sender=self.sender, receiver=self.receiver, message=message)
