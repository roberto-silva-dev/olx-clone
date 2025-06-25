import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from anuncios.models import Categoria, Anuncio
from django.contrib.auth.models import User

def criar_dados_exemplo():
    # Criar usuário de exemplo
    usuario, criado = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if criado:
        usuario.set_password('test123')
        usuario.save()
        print('Usuário de teste criado')
    
    # Criar categorias
    dados_categorias = [
        {'nome': 'Eletrônicos', 'slug': 'eletronicos'},
        {'nome': 'Veículos', 'slug': 'veiculos'},
        {'nome': 'Imóveis', 'slug': 'imoveis'},
        {'nome': 'Serviços', 'slug': 'servicos'},
        {'nome': 'Vagas de Emprego', 'slug': 'vagas-emprego'},
        {'nome': 'Moda e Beleza', 'slug': 'moda-beleza'},
        {'nome': 'Casa e Jardim', 'slug': 'casa-jardim'},
        {'nome': 'Esportes e Lazer', 'slug': 'esportes-lazer'},
    ]
    
    categorias = {}
    for dados_cat in dados_categorias:
        categoria, criado = Categoria.objects.get_or_create(
            slug=dados_cat['slug'],
            defaults={'nome': dados_cat['nome']}
        )
        categorias[dados_cat['slug']] = categoria
        if criado:
            print(f'Categoria criada: {categoria.nome}')
    
    # Criar anúncios de exemplo
    dados_anuncios = [
        {
            'titulo': 'iPhone 13 Pro Max 128GB',
            'descricao': 'iPhone em excelente estado, pouco usado. Inclui carregador e capa.',
            'preco': Decimal('4500.00'),
            'condicao': 'usado',
            'categoria': categorias['eletronicos'],
            'localizacao': 'São Paulo, SP'
        },
        {
            'titulo': 'Honda Civic 2018',
            'descricao': 'Civic EXL 2018, automático, completo, 45.000 km. Documentação em dia.',
            'preco': Decimal('85000.00'),
            'condicao': 'usado',
            'categoria': categorias['veiculos'],
            'localizacao': 'Rio de Janeiro, RJ'
        },
        {
            'titulo': 'Apartamento 2 quartos',
            'descricao': 'Apto 2 quartos, sala, cozinha, banheiro. Próximo ao metrô.',
            'preco': Decimal('1200.00'),
            'condicao': 'novo',
            'categoria': categorias['imoveis'],
            'localizacao': 'Belo Horizonte, MG'
        },
        {
            'titulo': 'Notebook Dell Inspiron',
            'descricao': 'Notebook Dell Inspiron 15, i5, 8GB RAM, 256GB SSD. Novo na caixa.',
            'preco': Decimal('2800.00'),
            'condicao': 'novo',
            'categoria': categorias['eletronicos'],
            'localizacao': 'Curitiba, PR'
        },
        {
            'titulo': 'Bicicleta Caloi 10',
            'descricao': 'Bicicleta Caloi 10, aro 26, 18 marchas. Bem conservada.',
            'preco': Decimal('800.00'),
            'condicao': 'usado',
            'categoria': categorias['esportes-lazer'],
            'localizacao': 'Porto Alegre, RS'
        },
        {
            'titulo': 'Sofá 3 lugares',
            'descricao': 'Sofá 3 lugares, tecido azul, pouco usado. Entrega incluída.',
            'preco': Decimal('1200.00'),
            'condicao': 'usado',
            'categoria': categorias['casa-jardim'],
            'localizacao': 'Salvador, BA'
        },
        {
            'titulo': 'Desenvolvedor Python',
            'descricao': 'Vaga para desenvolvedor Python, experiência com Django. Home office.',
            'preco': Decimal('5000.00'),
            'condicao': 'novo',
            'categoria': categorias['vagas-emprego'],
            'localizacao': 'Remoto'
        },
        {
            'titulo': 'Tênis Nike Air Max',
            'descricao': 'Tênis Nike Air Max 270, número 42, novo. Cor preta.',
            'preco': Decimal('350.00'),
            'condicao': 'novo',
            'categoria': categorias['moda-beleza'],
            'localizacao': 'Fortaleza, CE'
        }
    ]
    
    for dados_anuncio in dados_anuncios:
        anuncio, criado = Anuncio.objects.get_or_create(
            titulo=dados_anuncio['titulo'],
            defaults={
                'descricao': dados_anuncio['descricao'],
                'preco': dados_anuncio['preco'],
                'condicao': dados_anuncio['condicao'],
                'categoria': dados_anuncio['categoria'],
                'localizacao': dados_anuncio['localizacao'],
                'usuario': usuario
            }
        )
        if criado:
            print(f'Anúncio criado: {anuncio.titulo}')
    
    print('\nDados de exemplo criados com sucesso!')
    print(f'Total de categorias: {Categoria.objects.count()}')
    print(f'Total de anúncios: {Anuncio.objects.count()}')

if __name__ == '__main__':
    criar_dados_exemplo() 