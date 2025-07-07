from django.db import models
from django.contrib.auth.models import User
from anuncios.models import Anuncio

# Create your models here.

class Chat(models.Model):
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE, related_name='chats')
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat entre {self.user1} e {self.user2} sobre {self.anuncio}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}: {self.content[:20]}..."
