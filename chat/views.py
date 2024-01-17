from .models import Conversation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import User
from .serializers import ConversationListSerializer, ConversationSerializer, UserSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse, render
from django.http import JsonResponse

# Create your views here.

# @csrf_exempt                                                              # Decorator to make the view csrf excempt.
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:                                                                      # If PrimaryKey (id) of the user is specified in the url
            users = User.objects.filter(id=pk)              # Select only that particular user
        else:
            user_names_dict = {}
            users = User.objects.all()
            for user in users:
                user_names_dict[user.name] = user.name
        serializer = UserSerializer(users, many=True, context={'request': request})
        return render(request, 'chat/index.html', {'users': user_names_dict})            # Return serialized data
    elif request.method == 'POST':
        data = JSONParser().parse(request)           # On POST, parse the request object to obtain the data in json
        serializer = UserSerializer(data=data)        # Seraialize the data
        if serializer.is_valid():
            serializer.save()                                            # Save it if valid
            return JsonResponse(serializer.data, status=201)     # Return back the data on success
        return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
def start_convo(request, ):
    data = request.data
    name = data.pop('name')
    try:
        participant = User.objects.get(name=name)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a non existent user'})

    conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                               Q(initiator=participant, receiver=request.user))
    if conversation.exists():
        return redirect(reverse('get_conversation', args=(conversation[0].id,)))
    else:
        conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
        return Response(ConversationSerializer(instance=conversation).data)


@api_view(['GET'])
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Conversation does not exist'})
    else:
        serializer = ConversationSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['GET'])
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(initiator=request.user) |
                                                    Q(receiver=request.user))
    serializer = ConversationListSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)

def chat_window(request, name):
    user = User.objects.get(name=name)
    receiver_id = user.id
    return render(request, 'chat/chat_window.html', {'selected_user': name, 'receiver_id': receiver_id})