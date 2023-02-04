''' Models for the chat app '''
from django.conf import settings
from django.db import models


class ChatMessage(models.Model):
    ''' To store chat messages '''
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sender')
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
