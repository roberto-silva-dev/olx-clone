from django.contrib import admin
from .models import Categoria, Anuncio, ImagemAnuncio

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'categoria_pai']
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ['nome']

@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'preco', 'categoria', 'localizacao', 'usuario', 'data_criacao', 'ativo']
    list_filter = ['categoria', 'condicao', 'ativo', 'data_criacao']
    search_fields = ['titulo', 'descricao', 'localizacao']
    list_editable = ['ativo']

@admin.register(ImagemAnuncio)
class ImagemAnuncioAdmin(admin.ModelAdmin):
    list_display = ['anuncio', 'ordem', 'data_upload']
    list_filter = ['data_upload']
    search_fields = ['anuncio__titulo']
