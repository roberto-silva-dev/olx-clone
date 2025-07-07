import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .models import Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Verifica se o usuário está autenticado
        if not self.scope['user'].is_authenticated:
            await self.close()
            return

        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        # Verifica se o usuário tem permissão para acessar este chat
        if not await self.can_access_chat():
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message'].strip()
            
            if not message:
                return
                
            sender_id = self.scope['user'].id
            chat_id = self.chat_id

            # Save message to DB
            await self.save_message(chat_id, sender_id, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                    'username': self.scope['user'].username,
                }
            )
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'username': username,
        }))

    @database_sync_to_async
    def can_access_chat(self):
        """Verifica se o usuário pode acessar este chat"""
        try:
            chat = Chat.objects.get(id=self.chat_id)
            return self.scope['user'] in [chat.user1, chat.user2]
        except Chat.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, chat_id, sender_id, message):
        """Salva a mensagem no banco de dados"""
        try:
            chat = Chat.objects.get(id=chat_id)
            sender = User.objects.get(id=sender_id)
            return Message.objects.create(chat=chat, sender=sender, content=message)
        except (Chat.DoesNotExist, User.DoesNotExist):
            return None 