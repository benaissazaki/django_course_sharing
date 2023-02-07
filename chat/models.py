''' Models for the chat app '''
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Max

User = get_user_model()


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

    def __str__(self) -> str:
        return f"{self.sender} to {self.receiver}"

    @staticmethod
    def get_unique_senders_last_message(receiver):
        """
            Returns a list of dictionaries containing the sender
            and the last message sent to the user
        """
        messages = ChatMessage.objects.filter(receiver=receiver) \
            .values('sender') \
            .annotate(max_timestamp=Max('timestamp'))
        unique_senders = [
            {
                'sender': User.objects.get(id=message['sender']),
                'last_message': ChatMessage
                    .objects
                    .get(sender=message['sender'], timestamp=message['max_timestamp'])
                    .message
            }
            for message in messages
        ]

        return unique_senders
