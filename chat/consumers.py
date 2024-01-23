import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile

from account.models import User
from .models import Message, ChatRoom
from .serializers import MessageSerializer
from channels.layers import get_channel_layer

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from django.contrib.auth.models import AnonymousUser
from account.models import Token
from urllib.parse import parse_qs
from jwt import decode, exceptions
from rest_framework_simplejwt.tokens import AccessToken
from account.models import User
from channels.db import database_sync_to_async
import uuid

def generate_personal_chat_room(user_1, user_2):
    # Ensure to create a unique room name
    unique_name = uuid.uuid4()
    return unique_name

def get_email_from_user_ids(user_ids):
    users = await database_sync_to_async(User.objects.filter)(id__in=user_ids)
    emails = [user.email for user in users]
    return emails

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self, *args, **kwargs):
        self.token = await self.get_token_from_query_params()
        self.user = await self.get_user_from_token()
        self.scope['user'] = self.user

        # self.room_name = self.scope["url_route"]["kwargs"]["id"]
        self.receiver = int(self.scope["url_route"]["kwargs"]["id"])
        # self.room_group_name = f"chat_{self.room_name}"

        self.room_name = generate_personal_chat_room(self.user, self.receiver)
        self.room_group_name = f"chat_{self.room_name}"
        print(self.room_group_name, 'room_group_name')

        self.user_ids = [self.user, self.receiver]
        self.emails = await get_email_from_user_ids(self.user_ids)
        print(self.emails, '<- self.emails')
        self.participants = []
        chat_room, created = await database_sync_to_async(ChatRoom.objects.get_or_create)(name=self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user': self.user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        raise StopConsumer()

    async def get_token_from_query_params(self):
        query_string = self.scope.get("query_string", b"").decode("utf-8")
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]
        return token

    @database_sync_to_async
    def get_user_from_token(self):
        try:
            decoded_token = AccessToken(self.token)
            user = decoded_token['user_id']
            # user = User.objects.get(id=user)
            print(user)
            return user
        except exceptions.ExpiredSignatureError:
        # Handle the case where the token has expired
            return None
        except (exceptions.InvalidTokenError, exceptions.DecodeError):
        # Handle invalid or malformed tokens
            return None















































#     # Receive message from WebSocket
#     async def receive(self, text_data=None, bytes_data=None):
#         # parse the json data into dictionary object
#         text_data_json = json.loads(text_data)

#         # # Send message to room group
#         # chat_type = {"type": "chat_message"}
#         # return_dict = {**chat_type, **text_data_json}
#         # await self.channel_layer.group_send(
#         #     self.room_group_name,
#         #     return_dict,
#         # )

#     # Receive message from room group
#     # async def chat_message(self, event):
#     #     text_data_json = event.copy()
#     #     text_data_json.pop("type")
#     #     message, attachment = (
#     #         text_data_json["message"],
#     #         text_data_json.get("attachment"),
#     #     )

#     #     conversation = Conversation.objects.get(id=int(self.room_name))
#     #     sender = self.scope['user']

#     #     # Attachment
#     #     if attachment:
#     #         file_str, file_ext = attachment["data"], attachment["format"]

#     #         file_data = ContentFile(
#     #             base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
#     #         )
#     #         _message = Message.objects.create(
#     #             sender=sender,
#     #             attachment=file_data,
#     #             text=message,
#     #             conversation_id=conversation,
#     #         )
#     #     else:
#     #         _message = Message.objects.create(
#     #             sender=sender,
#     #             text=message,
#     #             conversation_id=conversation,
#     #         )
#     #     serializer = MessageSerializer(instance=_message)
#     #     # Send message to WebSocket
#     #     self.send(
#     #         text_data=json.dumps(
#     #             serializer.data
#     #         )
#     #     )

#     @database_sync_to_async
#     def get_user(self):
#         # Retrieve the user from the scope
#         return self.scope.get('user')

# def generate_chat_room_name(user1, user2):
#     # Sort the usernames alphabetically
#     sorted_usernames = sorted([user1, user2])

#     # Concatenate the sorted usernames to create the chat room name
#     chat_room_name = f"room_{sorted_usernames[0]}_{sorted_usernames[1]}"

#     return chat_room_name