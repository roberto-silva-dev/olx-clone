from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from anuncios.models import Anuncio, Categoria

# Create your views here.

def registrar(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')
    else:
        formulario = UserCreationForm()
    return render(request, 'authapp/register.html', {'form': formulario})

def logout_view(request):
    """View personalizada para logout que aceita GET e POST"""
    logout(request)
    messages.success(request, 'Você saiu com sucesso!')
    return redirect('home')

def home(request):
    # Obter parâmetros de pesquisa
    consulta = request.GET.get('q', '')
    categoria = request.GET.get('categoria', '')
    condicao = request.GET.get('condicao', '')
    preco_minimo = request.GET.get('preco_minimo', '')
    preco_maximo = request.GET.get('preco_maximo', '')
    
    # Filtrar anúncios
    anuncios = Anuncio.objects.filter(ativo=True)
    
    if consulta:
        anuncios = anuncios.filter(
            Q(titulo__icontains=consulta) | 
            Q(descricao__icontains=consulta) |
            Q(localizacao__icontains=consulta)
        )
    
    if categoria:
        anuncios = anuncios.filter(categoria__slug=categoria)
    
    if condicao:
        anuncios = anuncios.filter(condicao=condicao)
    
    if preco_minimo:
        anuncios = anuncios.filter(preco__gte=preco_minimo)
    
    if preco_maximo:
        anuncios = anuncios.filter(preco__lte=preco_maximo)
    
    # Ordenar por mais recentes
    anuncios = anuncios.order_by('-data_criacao')
    
    # Obter categorias para filtros
    categorias = Categoria.objects.all()
    
    contexto = {
        'anuncios': anuncios,
        'categorias': categorias,
        'consulta': consulta,
        'categoria_selecionada': categoria,
        'condicao_selecionada': condicao,
        'preco_minimo': preco_minimo,
        'preco_maximo': preco_maximo,
    }
    
    return render(request, 'authapp/home.html', contexto)
