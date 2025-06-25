from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    categoria_pai = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategorias')
    
    class Meta:
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return self.nome

class Anuncio(models.Model):
    CONDICAO_CHOICES = [
        ('novo', 'Novo'),
        ('usado', 'Usado'),
        ('reformado', 'Reformado'),
    ]
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    condicao = models.CharField(max_length=20, choices=CONDICAO_CHOICES, default='usado')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    localizacao = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
    
    def get_imagem_principal(self):
        """Retorna a primeira imagem do anúncio ou None"""
        return self.imagens.first()

class ImagemAnuncio(models.Model):
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='anuncios/')
    ordem = models.PositiveIntegerField(default=0)
    data_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['ordem']
    
    def __str__(self):
        return f"Imagem {self.ordem} - {self.anuncio.titulo}"
