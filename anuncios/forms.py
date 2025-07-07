from django import forms
from .models import Anuncio, ImagemAnuncio

class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['titulo', 'descricao', 'preco', 'condicao', 'categoria', 'localizacao']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: iPhone 13 Pro Max 128GB - Excelente estado',
                'maxlength': '200'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 6, 
                'placeholder': 'Descreva detalhadamente o produto/serviço, incluindo características, especificações, estado de conservação, acessórios incluídos, etc.'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '0,00',
                'min': '0',
                'step': '0.01'
            }),
            'condicao': forms.Select(attrs={
                'class': 'form-select'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'localizacao': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: São Paulo, SP'
            }),
        }
        
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo.strip()) < 10:
            raise forms.ValidationError('O título deve ter pelo menos 10 caracteres.')
        return titulo.strip()
    
    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao')
        if len(descricao.strip()) < 20:
            raise forms.ValidationError('A descrição deve ter pelo menos 20 caracteres.')
        return descricao.strip()
    
    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco <= 0:
            raise forms.ValidationError('O preço deve ser maior que zero.')
        return preco

class ImagemAnuncioForm(forms.ModelForm):
    class Meta:
        model = ImagemAnuncio
        fields = ['imagem']
        widgets = {
            'imagem': forms.FileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*',
                'style': 'display: none;'
            })
        }
    
    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem')
        if imagem:
            # Verificar tamanho do arquivo (máx 5MB)
            if imagem.size > 5 * 1024 * 1024:
                raise forms.ValidationError('A imagem deve ter no máximo 5MB.')
            
            # Verificar tipo de arquivo
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if imagem and getattr(imagem, 'content_type', '') not in allowed_types:
                raise forms.ValidationError('Formato de imagem não suportado. Use JPG, PNG ou GIF.')
        
        return imagem 