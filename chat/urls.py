from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('seller/', views.seller_chats, name='seller_chats'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('start/<int:anuncio_id>/', views.start_chat, name='start_chat'),
] 