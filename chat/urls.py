''' Chat application's urls '''
from django.urls import path
from .views import chat_view, chat_list_view

urlpatterns = [
    path('', chat_list_view, name='chat-list'),
    path('<int:user_id>', chat_view, name='chat')
]
