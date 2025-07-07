from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from anuncios.models import Anuncio
from .models import Chat, Message
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your views here.

@login_required
def chat_view(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, pk=anuncio_id)
    if request.user == anuncio.usuario:
        return redirect('detalhes_anuncio', pk=anuncio_id)
    # Busca ou cria o chat entre o usuário logado e o anunciante
    chat, created = Chat.objects.get_or_create(
        anuncio=anuncio,
        user1=min(request.user, anuncio.usuario, key=lambda u: u.id),
        user2=max(request.user, anuncio.usuario, key=lambda u: u.id),
    )
    messages = chat.messages.order_by('timestamp')
    return render(request, 'chat/chat.html', {
        'chat': chat,
        'anuncio': anuncio,
        'messages': messages,
    })

@login_required
def chat_list(request):
    """Lista todos os chats do usuário logado"""
    # Busca todos os chats onde o usuário participa
    chats = Chat.objects.filter(
        user1=request.user
    ) | Chat.objects.filter(
        user2=request.user
    ).order_by('-created_at')
    
    # Para cada chat, pega a última mensagem
    unread_chats_count = 0
    for chat in chats:
        last_message = chat.messages.order_by('-timestamp').first()
        chat.last_message = last_message
        # Determina o outro usuário do chat
        if chat.user1 == request.user:
            chat.other_user = chat.user2
        else:
            chat.other_user = chat.user1
        
        # Conta mensagens não lidas (mensagens do outro usuário que não foram lidas)
        unread_messages = chat.messages.filter(
            sender=chat.other_user,
            is_read=False
        ).count()
        chat.unread_count = unread_messages
        chat.has_unread_messages = unread_messages > 0
        
        if chat.has_unread_messages:
            unread_chats_count += 1
        
        # Verifica se é uma conversa recente (última mensagem nos últimos 7 dias)
        if chat.last_message:
            seven_days_ago = datetime.now() - timedelta(days=7)
            chat.is_recent = chat.last_message.timestamp.replace(tzinfo=None) > seven_days_ago
        else:
            chat.is_recent = False
    
    # Aplica filtros se fornecidos
    filter_unread = request.GET.get('unread', '')
    filter_recent = request.GET.get('recent', '')
    
    if filter_unread == 'true':
        chats = [chat for chat in chats if chat.has_unread_messages]
    
    if filter_recent == 'true':
        chats = [chat for chat in chats if chat.is_recent]
    
    return render(request, 'chat/chat_list.html', {
        'chats': chats,
        'filter_unread': filter_unread,
        'filter_recent': filter_recent,
        'unread_chats_count': unread_chats_count,
    })

@login_required
def chat_detail(request, chat_id):
    """Visualiza um chat específico"""
    chat = get_object_or_404(Chat, pk=chat_id)
    
    # Verifica se o usuário tem permissão para ver este chat
    if request.user not in [chat.user1, chat.user2]:
        return redirect('chat_list')
    
    # Determina o outro usuário do chat
    if chat.user1 == request.user:
        other_user = chat.user2
    else:
        other_user = chat.user1
    
    # Busca todas as mensagens do chat ordenadas por timestamp
    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    
    # Marca as mensagens do outro usuário como lidas
    messages.filter(sender=other_user, is_read=False).update(is_read=True)
    
    return render(request, 'chat/chat_detail.html', {
        'chat': chat,
        'other_user': other_user,
        'anuncio': chat.anuncio,
        'messages': messages,
    })

@login_required
def start_chat(request, anuncio_id):
    """Inicia um novo chat sobre um anúncio"""
    anuncio = get_object_or_404(Anuncio, pk=anuncio_id)
    
    # Verifica se o usuário não é o anunciante
    if request.user == anuncio.usuario:
        return redirect('detalhes_anuncio', pk=anuncio_id)
    
    # Busca ou cria o chat entre o usuário logado e o anunciante
    chat, created = Chat.objects.get_or_create(
        anuncio=anuncio,
        user1=min(request.user, anuncio.usuario, key=lambda u: u.id),
        user2=max(request.user, anuncio.usuario, key=lambda u: u.id),
    )
    
    return redirect('chat_detail', chat_id=chat.id)

@login_required
def seller_chats(request):
    """Lista todos os chats dos anúncios do vendedor"""
    # Busca todos os anúncios do usuário
    user_anuncios = Anuncio.objects.filter(usuario=request.user)
    
    # Busca todos os chats relacionados aos anúncios do usuário
    chats = Chat.objects.filter(anuncio__in=user_anuncios).order_by('-created_at')
    
    # Para cada chat, pega a última mensagem e determina o comprador
    active_chats_count = 0
    for chat in chats:
        last_message = chat.messages.order_by('-timestamp').first()
        chat.last_message = last_message
        # Determina o comprador (usuário que não é o anunciante)
        if chat.user1 == request.user:
            chat.buyer = chat.user2
        else:
            chat.buyer = chat.user1
        
        # Conta mensagens não lidas (mensagens do comprador que não foram lidas pelo vendedor)
        unread_messages = chat.messages.filter(
            sender=chat.buyer,
            is_read=False
        ).count()
        chat.unread_count = unread_messages
        
        # Marca se tem novas mensagens
        chat.has_new_messages = unread_messages > 0
        if chat.has_new_messages:
            active_chats_count += 1
    
    # Aplica filtros se fornecidos
    filter_new = request.GET.get('new', '')
    if filter_new == 'true':
        chats = [chat for chat in chats if chat.has_new_messages]
    
    return render(request, 'chat/seller_chats.html', {
        'chats': chats,
        'filter_new': filter_new,
        'active_chats_count': active_chats_count,
    })
