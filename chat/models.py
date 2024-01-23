from django.db import models
from account.models import User

# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', null=True)





















# class Conversation(models.Model):
#     initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="convo_starter")
#     receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="convo_participant")
#     start_time = models.DateTimeField(auto_now_add=True)


# class Message(models.Model):
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='message_sender')
#     text = models.CharField(max_length=200, blank=True)
#     attachment = models.FileField(blank=True)
#     conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE,)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ('-timestamp',)