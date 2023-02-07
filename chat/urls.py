''' Chat application's urls '''
from django.urls import path
from .views import chat_view, chat_list_view

urlpatterns = [
    path('', chat_list_view, name='chat-list'),
    path('chat/<int:user_id>', chat_view, name='chat'),
    path('chat', chat_view, {'user_id': 0}, name='chat-with-admin')
]
