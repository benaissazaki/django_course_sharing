''' Chat app views '''
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import ChatMessage

User = get_user_model()

admin = User.objects.get(is_superuser=True).id

@login_required
def chat_view(request, user_id):
    ''' Render chat template '''
    if request.user.is_superuser:
        previous_messages = ChatMessage.objects\
            .filter(
                Q(sender=request.user, receiver=user_id) |
                Q(sender=user_id, receiver=request.user)
            ) \
            .order_by('timestamp')

    else:
        previous_messages = ChatMessage.objects\
            .filter(
                Q(sender=request.user, receiver=admin) |
                Q(sender=admin, receiver=request.user)
            ) \
            .order_by('timestamp')

    return render(request,
                  'chat/chat.html',
                  {'user_id': user_id, 'previous_messages': previous_messages})


@user_passes_test(lambda user: user.is_superuser, 'chat-with-admin')
def chat_list_view(request):
    '''
        Renders a template showing links to multiple chats.
    '''
    senders = ChatMessage.get_unique_senders_last_message(request.user)

    return render(request, 'chat/index.html', {'senders': senders})
