from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from a_inbox import forms as inbox_forms
from a_inbox import models as inbox_models
from a_users import models as user_models

f = Fernet(settings.ENCRYPT_KEY)


@login_required
def inbox_view(request, conversation_id=None):
    my_conversations = inbox_models.Conversation.objects.filter(
        participants=request.user,
    )

    if conversation_id:
        conversation = get_object_or_404(my_conversations, id=conversation_id)
        latest_message = conversation.messages.first()
        if not conversation.is_seen and latest_message.sender != request.user:
            conversation.is_seen = True
            conversation.save()
    else:
        conversation = None

    context = {
        'conversation': conversation,
        'my_conversations': my_conversations,
    }
    return render(request, 'a_inbox/inbox.html', context)


def search_users(request):
    letters = request.GET.get('search_user')
    if request.htmx:
        if len(letters) > 0:
            profiles = user_models.Profile.objects.filter(
                realname__icontains=letters).exclude(realname=request.user.profile.realname)
            users_id = profiles.values_list('user', flat=True)
            users = User.objects.filter(
                Q(username__icontains=letters) | Q(id__in=users_id)
            ).exclude(username=request.user.username)
            context = {
                'users': users,
            }
            return render(request, 'a_inbox/list_search_user.html', context)
        else:
            return HttpResponse('')
    else:
        raise Http404()


@login_required
def new_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    new_message_form = inbox_forms.InboxNewMessageForm()

    if request.method == 'POST':
        form = inbox_forms.InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            # encrypt message
            message_original = form.cleaned_data['body']
            message_bytes = message_original.encode('utf-8')
            message_encrypted = f.encrypt(message_bytes)
            message_decoded = message_encrypted.decode('utf-8')
            message.body = message_decoded

            message.sender = request.user

            my_conversations = request.user.conversations.all()
            for c in my_conversations:
                if recipient in c.participants.all():
                    message.conversation = c
                    message.save()
                    c.last_message_created = timezone.now()
                    c.is_seen = False
                    c.save()
                    return redirect('inbox', c.id)

            new_conversation = inbox_models.Conversation.objects.create()
            new_conversation.participants.add(request.user, recipient)
            new_conversation.save()
            message.conversation = new_conversation
            message.save()
            return redirect('inbox', new_conversation.id)

    context = {
        'recipient': recipient,
        'new_message_form': new_message_form,
    }
    return render(request, 'a_inbox/form_new_message.html', context)


@login_required
def new_reply(request, conversation_id):
    new_message_form = inbox_forms.InboxNewMessageForm()
    my_conversations = request.user.conversations.all()
    conversation = get_object_or_404(my_conversations, id=conversation_id)

    if request.method == 'POST':
        form = inbox_forms.InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            # encrypt message
            message_original = form.cleaned_data['body']
            message_bytes = message_original.encode('utf-8')
            message_encrypted = f.encrypt(message_bytes)
            message_decoded = message_encrypted.decode('utf-8')
            message.body = message_decoded

            message.sender = request.user
            message.conversation = conversation
            message.save()
            conversation.last_message_created = timezone.now()
            conversation.is_seen = False
            conversation.save()
            return redirect('inbox', conversation.id)

    context = {
        'new_message_form': new_message_form,
        'conversation': conversation,
    }
    return render(request, 'a_inbox/form_new_reply.html', context)


@login_required
def notify_new_message(request, conversation_id):
    conversation = get_object_or_404(inbox_models.Conversation, id=conversation_id)
    latest_message = conversation.messages.first()
    if not conversation.is_seen and latest_message.sender != request.user:
        return render(request, 'a_inbox/notify_icon.html')
    else:
        return HttpResponse('')


def notify_inbox(request):
    my_conversations = inbox_models.Conversation.objects.filter(
        participants=request.user, is_seen=False,
    )
    for c in my_conversations:
        latest_message = c.messages.first()
        if latest_message.sender != request.user:
            return render(request, 'a_inbox/notify_icon.html')
    return HttpResponse('')