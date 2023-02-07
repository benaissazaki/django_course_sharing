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
        if self.sender.is_superuser:
            receiver_id = self.scope['url_route']['kwargs']['user_id']
            self.receiver = await database_sync_to_async(self.get_user)(user_id=receiver_id)
        else:
            self.receiver = await database_sync_to_async(self.get_superuser)()

        if not self.sender.is_authenticated or not self.receiver:
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

    async def chat_message(self, event):
        ''' Send a reply to the received chat message '''
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    def get_superuser(self):
        ''' Get superuser from database  '''
        return get_user_model().objects.filter(
            is_superuser=True).first()

    def new_message(self, message):
        ''' Create new message in database '''
        ChatMessage.objects.create(
            sender=self.sender, receiver=self.receiver, message=message)

    def get_user(self, user_id):
        ''' Get a user from the db by its id '''
        return get_user_model().objects.get(id=user_id)
