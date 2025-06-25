from django import forms
from .models import Anuncio, ImagemAnuncio

class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['titulo', 'descricao', 'preco', 'condicao', 'categoria', 'localizacao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do anúncio'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva seu produto/serviço'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0,00'}),
            'condicao': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade, Estado'}),
        }

class ImagemAnuncioForm(forms.ModelForm):
    class Meta:
        model = ImagemAnuncio
        fields = ['imagem']
        widgets = {
            'imagem': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        } 