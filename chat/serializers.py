from account.serializers import UserSerializer
from rest_framework import serializers
from .models import ChatRoom, Message

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'participants']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'chat_room']









# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         exclude = ('conversation_id',)


# class ConversationListSerializer(serializers.ModelSerializer):
#     initiator = UserSerializer()
#     receiver = UserSerializer()
#     last_message = serializers.SerializerMethodField()

#     class Meta:
#         model = Conversation
#         fields = ['initiator', 'receiver', 'last_message']

#     def get_last_message(self, instance):
#         message = instance.message_set.first()
#         if message:
#             message_serializer = MessageSerializer(instance=message)
#             return message_serializer.data
#         return None


# class ConversationSerializer(serializers.ModelSerializer):
#     initiator = UserSerializer()
#     receiver = UserSerializer()
#     message_set = MessageSerializer(many=True)

#     class Meta:
#         model = Conversation
#         fields = ['initiator', 'receiver', 'message_set']
