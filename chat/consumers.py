import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile

from account.models import User
from .models import Message, Conversation
from .serializers import MessageSerializer
from channels.layers import get_channel_layer

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self, *args, **kwargs):
        self.room_name = self.scope["url_route"]["kwargs"]["id"]
        self.room_group_name = f"chat_{self.room_name}"

        self.user = await self.get_user()

        # print(self.room_group_name)
        print(self.user)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,   # group discard
            self.channel_name
        )
        raise StopConsumer()
    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)

        # # Send message to room group
        # chat_type = {"type": "chat_message"}
        # return_dict = {**chat_type, **text_data_json}
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     return_dict,
        # )

    # Receive message from room group
    # async def chat_message(self, event):
    #     text_data_json = event.copy()
    #     text_data_json.pop("type")
    #     message, attachment = (
    #         text_data_json["message"],
    #         text_data_json.get("attachment"),
    #     )

    #     conversation = Conversation.objects.get(id=int(self.room_name))
    #     sender = self.scope['user']

    #     # Attachment
    #     if attachment:
    #         file_str, file_ext = attachment["data"], attachment["format"]

    #         file_data = ContentFile(
    #             base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
    #         )
    #         _message = Message.objects.create(
    #             sender=sender,
    #             attachment=file_data,
    #             text=message,
    #             conversation_id=conversation,
    #         )
    #     else:
    #         _message = Message.objects.create(
    #             sender=sender,
    #             text=message,
    #             conversation_id=conversation,
    #         )
    #     serializer = MessageSerializer(instance=_message)
    #     # Send message to WebSocket
    #     self.send(
    #         text_data=json.dumps(
    #             serializer.data
    #         )
    #     )

    @database_sync_to_async
    def get_user(self):
        # Retrieve the user from the scope
        return self.scope.get('user')

def generate_chat_room_name(user1, user2):
    # Sort the usernames alphabetically
    sorted_usernames = sorted([user1, user2])

    # Concatenate the sorted usernames to create the chat room name
    chat_room_name = f"room_{sorted_usernames[0]}_{sorted_usernames[1]}"

    return chat_room_name