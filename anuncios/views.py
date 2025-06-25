from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from django.db import transaction
from .models import Anuncio, Categoria, ImagemAnuncio
from .forms import AnuncioForm, ImagemAnuncioForm

# Create your views here.

@login_required
def criar_anuncio(request):
    # Criar o formset factory sem formset personalizado
    ImagemAnuncioFormSet = modelformset_factory(
        ImagemAnuncio, 
        form=ImagemAnuncioForm, 
        extra=6, 
        max_num=6,
        can_delete=True
    )
    
    if request.method == 'POST':
        form_anuncio = AnuncioForm(request.POST)
        formset_imagens = ImagemAnuncioFormSet(request.POST, request.FILES, prefix='imagens')
        
        # Debug: verificar se os formulários são válidos
        print(f"Form anúncio válido: {form_anuncio.is_valid()}")
        if not form_anuncio.is_valid():
            print(f"Erros do form anúncio: {form_anuncio.errors}")
        
        print(f"Formset imagens válido: {formset_imagens.is_valid()}")
        if not formset_imagens.is_valid():
            print(f"Erros do formset: {formset_imagens.errors}")
        
        # Verificar se há imagens sendo enviadas
        imagens_enviadas = 0
        for form in formset_imagens:
            if form.cleaned_data and form.cleaned_data.get('imagem'):
                imagens_enviadas += 1
        print(f"Imagens enviadas: {imagens_enviadas}")
        
        if form_anuncio.is_valid():
            try:
                with transaction.atomic():
                    # Salvar anúncio
                    anuncio = form_anuncio.save(commit=False)
                    anuncio.usuario = request.user
                    anuncio.save()
                    print(f"Anúncio salvo com ID: {anuncio.id}")
                    
                    # Salvar imagens (se o formset for válido)
                    imagens_salvas = 0
                    if formset_imagens.is_valid():
                        for form_imagem in formset_imagens:
                            if form_imagem.cleaned_data and not form_imagem.cleaned_data.get('DELETE'):
                                if form_imagem.cleaned_data.get('imagem'):  # Verificar se há imagem
                                    imagem = form_imagem.save(commit=False)
                                    imagem.anuncio = anuncio
                                    imagem.ordem = imagens_salvas
                                    imagem.save()
                                    imagens_salvas += 1
                                    print(f"Imagem salva: {imagem.imagem.name}")
                    
                    messages.success(request, f'Anúncio criado com sucesso! {imagens_salvas} imagem(s) salva(s).')
                    return redirect('home')
                    
            except Exception as e:
                messages.error(request, f'Erro ao criar anúncio: {str(e)}')
                print(f"Erro: {e}")
        else:
            # Se o formulário de anúncio não é válido, mostrar erros
            for field, errors in form_anuncio.errors.items():
                for error in errors:
                    messages.error(request, f'Erro no campo {field}: {error}')
    else:
        form_anuncio = AnuncioForm()
        formset_imagens = ImagemAnuncioFormSet(prefix='imagens')
    
    categorias = Categoria.objects.all()
    contexto = {
        'form_anuncio': form_anuncio,
        'formset_imagens': formset_imagens,
        'categorias': categorias,
    }
    
    return render(request, 'anuncios/criar_anuncio.html', contexto)

@login_required
def meus_anuncios(request):
    """Lista os anúncios do usuário logado"""
    anuncios = Anuncio.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    contexto = {
        'anuncios': anuncios,
        'titulo_pagina': 'Meus Anúncios'
    }
    
    return render(request, 'anuncios/meus_anuncios.html', contexto)

def detalhes_anuncio(request, pk):
    """Exibe os detalhes de um anúncio específico"""
    anuncio = get_object_or_404(Anuncio, pk=pk, ativo=True)
    
    # Buscar anúncios similares da mesma categoria
    anuncios_similares = Anuncio.objects.filter(
        categoria=anuncio.categoria,
        ativo=True
    ).exclude(pk=anuncio.pk).order_by('-data_criacao')[:6]
    
    contexto = {
        'anuncio': anuncio,
        'anuncios_similares': anuncios_similares,
        'titulo_pagina': anuncio.titulo
    }
    
    return render(request, 'anuncios/detalhes_anuncio.html', contexto)

@login_required
def editar_anuncio(request, pk):
    """Edita um anúncio existente"""
    anuncio = get_object_or_404(Anuncio, pk=pk, usuario=request.user)
    
    # Criar o formset factory
    ImagemAnuncioFormSet = modelformset_factory(
        ImagemAnuncio, 
        form=ImagemAnuncioForm, 
        extra=6, 
        max_num=6,
        can_delete=True
    )
    
    if request.method == 'POST':
        form_anuncio = AnuncioForm(request.POST, instance=anuncio)
        formset_imagens = ImagemAnuncioFormSet(request.POST, request.FILES, prefix='imagens')
        
        if form_anuncio.is_valid() and formset_imagens.is_valid():
            try:
                with transaction.atomic():
                    # Salvar anúncio
                    anuncio = form_anuncio.save()
                    
                    # Salvar imagens
                    imagens_salvas = 0
                    for form_imagem in formset_imagens:
                        if form_imagem.cleaned_data and not form_imagem.cleaned_data.get('DELETE'):
                            if form_imagem.cleaned_data.get('id'):
                                # Atualizar imagem existente
                                imagem = form_imagem.save(commit=False)
                                imagem.ordem = imagens_salvas
                                imagem.save()
                            else:
                                # Nova imagem
                                imagem = form_imagem.save(commit=False)
                                imagem.anuncio = anuncio
                                imagem.ordem = imagens_salvas
                                imagem.save()
                            imagens_salvas += 1
                        elif form_imagem.cleaned_data.get('id') and form_imagem.cleaned_data.get('DELETE'):
                            # Deletar imagem
                            form_imagem.instance.delete()
                    
                    messages.success(request, 'Anúncio atualizado com sucesso!')
                    return redirect('detalhes_anuncio', pk=anuncio.pk)
                    
            except Exception as e:
                messages.error(request, f'Erro ao atualizar anúncio: {str(e)}')
    else:
        form_anuncio = AnuncioForm(instance=anuncio)
        formset_imagens = ImagemAnuncioFormSet(
            queryset=anuncio.imagens.all(),
            prefix='imagens'
        )
    
    categorias = Categoria.objects.all()
    contexto = {
        'form_anuncio': form_anuncio,
        'formset_imagens': formset_imagens,
        'categorias': categorias,
        'anuncio': anuncio,
    }
    
    return render(request, 'anuncios/editar_anuncio.html', contexto)
