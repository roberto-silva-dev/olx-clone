from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_anuncio, name='criar_anuncio'),
    path('meus-anuncios/', views.meus_anuncios, name='meus_anuncios'),
    path('anuncio/<int:pk>/', views.detalhes_anuncio, name='detalhes_anuncio'),
    path('editar/<int:pk>/', views.editar_anuncio, name='editar_anuncio'),
    path('deletar/<int:pk>/', views.deletar_anuncio, name='deletar_anuncio'),
    # URLs para anúncios serão adicionadas aqui no futuro
    # path('anuncio/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
] 