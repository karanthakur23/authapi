from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_convo, name='start_convo'),
    path('<int:convo_id>/', views.get_conversation, name='get_conversation'),
    path('', views.conversations, name='conversations'),

    path('api/users/<int:pk>', views.user_list, name='user-detail'),      # GET request for user with id
    path('api/users/', views.user_list, name='user-list'),

    path('api/users/chat-window/<str:name>', views.chat_window, name='chat-window'),
]
