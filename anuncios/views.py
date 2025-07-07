from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import os
from .models import Anuncio, Categoria, ImagemAnuncio
from .forms import AnuncioForm, ImagemAnuncioForm

# Create your views here.

@login_required
def criar_anuncio(request):
    # Criar o formset factory
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
        
        if form_anuncio.is_valid():
            try:
                with transaction.atomic():
                    # Salvar anúncio
                    anuncio = form_anuncio.save(commit=False)
                    anuncio.usuario = request.user
                    anuncio.save()
                    
                    # Salvar imagens
                    imagens_salvas = 0
                    if formset_imagens.is_valid():
                        for form_imagem in formset_imagens:
                            if form_imagem.cleaned_data and not form_imagem.cleaned_data.get('DELETE'):
                                if form_imagem.cleaned_data.get('imagem'):
                                    imagem = form_imagem.save(commit=False)
                                    imagem.anuncio = anuncio
                                    imagem.ordem = imagens_salvas
                                    imagem.save()
                                    imagens_salvas += 1
                    
                    messages.success(request, f'Anúncio criado com sucesso! {imagens_salvas} imagem(s) salva(s).')
                    return redirect('home')
                    
            except Exception as e:
                messages.error(request, f'Erro ao criar anúncio: {str(e)}')
        else:
            # Mostrar erros de validação
            for field, errors in form_anuncio.errors.items():
                for error in errors:
                    messages.error(request, f'Erro no campo {field}: {error}')
    else:
        form_anuncio = AnuncioForm()
        formset_imagens = ImagemAnuncioFormSet(prefix='imagens')
    
    contexto = {
        'form_anuncio': form_anuncio,
        'formset_imagens': formset_imagens,
        'anuncio': None,  # Indica que é criação
    }
    
    return render(request, 'anuncios/anuncio_form.html', contexto)

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
        
        if form_anuncio.is_valid():
            try:
                with transaction.atomic():
                    # Salvar anúncio
                    anuncio = form_anuncio.save()
                    
                    # Processar imagens
                    imagens_salvas = 0
                    imagens_deletadas = 0
                    
                    # Primeiro, processar imagens existentes
                    for form_imagem in formset_imagens:
                        if form_imagem.cleaned_data:
                            if form_imagem.cleaned_data.get('DELETE') and form_imagem.cleaned_data.get('id'):
                                # Deletar imagem existente
                                imagem = form_imagem.instance
                                if os.path.exists(imagem.imagem.path):
                                    os.remove(imagem.imagem.path)
                                imagem.delete()
                                imagens_deletadas += 1
                            elif form_imagem.cleaned_data.get('id'):
                                # Manter imagem existente
                                imagem = form_imagem.instance
                                imagem.ordem = imagens_salvas
                                imagem.save()
                                imagens_salvas += 1
                            elif form_imagem.cleaned_data.get('imagem'):
                                # Nova imagem
                                imagem = form_imagem.save(commit=False)
                                imagem.anuncio = anuncio
                                imagem.ordem = imagens_salvas
                                imagem.save()
                                imagens_salvas += 1
                    
                    # Reordenar imagens restantes
                    for i, imagem in enumerate(anuncio.imagens.all().order_by('ordem')):
                        imagem.ordem = i
                        imagem.save()
                    
                    messages.success(request, f'Anúncio atualizado com sucesso! {imagens_salvas} imagem(s) salva(s), {imagens_deletadas} deletada(s).')
                    return redirect('detalhes_anuncio', pk=anuncio.pk)
                    
            except Exception as e:
                messages.error(request, f'Erro ao atualizar anúncio: {str(e)}')
        else:
            # Mostrar erros de validação
            if not form_anuncio.is_valid():
                for field, errors in form_anuncio.errors.items():
                    for error in errors:
                        messages.error(request, f'Erro no campo {field}: {error}')
            if not formset_imagens.is_valid():
                for form in formset_imagens:
                    if form.errors:
                        for field, errors in form.errors.items():
                            for error in errors:
                                messages.error(request, f'Erro na imagem: {error}')
    else:
        form_anuncio = AnuncioForm(instance=anuncio)
        formset_imagens = ImagemAnuncioFormSet(
            queryset=anuncio.imagens.all().order_by('ordem'),
            prefix='imagens'
        )
    
    contexto = {
        'form_anuncio': form_anuncio,
        'formset_imagens': formset_imagens,
        'anuncio': anuncio,  # Indica que é edição
    }
    
    return render(request, 'anuncios/anuncio_form.html', contexto)

@login_required
@require_POST
def deletar_anuncio(request, pk):
    """Deleta um anúncio (soft delete)"""
    anuncio = get_object_or_404(Anuncio, pk=pk, usuario=request.user)
    
    try:
        with transaction.atomic():
            # Deletar arquivos de imagem
            for imagem in anuncio.imagens.all():
                if os.path.exists(imagem.imagem.path):
                    os.remove(imagem.imagem.path)
            
            # Soft delete do anúncio
            anuncio.ativo = False
            anuncio.save()
            
            return JsonResponse({'success': True, 'message': 'Anúncio deletado com sucesso!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro ao deletar anúncio: {str(e)}'})
