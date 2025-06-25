import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='admin')
    user.set_password('admin')
    user.save()
    print('Senha do superuser "admin" foi definida como "admin" com sucesso!')
except User.DoesNotExist:
    print('Usuário "admin" não encontrado!') 