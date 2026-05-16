from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Perfil, Sistema, UsuarioSistema

NOME_SISTEMA_PRINCIPAL = 'SISCAU'
NOME_PERFIL_ADMINISTRADOR = 'Administrador'
NOME_PERFIL_PRODUTOR = 'Produtor'


def garantir_perfis_base():
    sistema, _ = Sistema.objects.get_or_create(
        nome=NOME_SISTEMA_PRINCIPAL,
        defaults={
            'descricao': 'Sistema principal de acesso ao SISCAU',
            'ativo': True,
        },
    )

    perfis_defaults = {
        NOME_PERFIL_ADMINISTRADOR: 'Perfil com permissão para cadastrar e administrar usuários.',
        NOME_PERFIL_PRODUTOR: 'Perfil padrão do produtor para operar o sistema.',
    }

    perfis = {}
    for nome, descricao in perfis_defaults.items():
        perfil, _ = Perfil.objects.get_or_create(
            nome=nome,
            sistema=sistema,
            defaults={
                'descricao': descricao,
                'ativo': True,
            },
        )
        if not perfil.ativo:
            perfil.ativo = True
            perfil.save(update_fields=['ativo'])
        perfis[nome] = perfil

    return sistema, perfis


def usuario_eh_administrador(user):
    if not getattr(user, 'is_authenticated', False):
        return False

    if user.is_superuser:
        return True

    return UsuarioSistema.objects.filter(
        usuario=user,
        ativo=True,
        sistema__nome=NOME_SISTEMA_PRINCIPAL,
        perfil__nome=NOME_PERFIL_ADMINISTRADOR,
        perfil__ativo=True,
    ).exists()


def administrador_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        garantir_perfis_base()
        if not usuario_eh_administrador(request.user):
            messages.error(
                request,
                'Apenas usuários com perfil Administrador podem cadastrar usuários no sistema.',
            )
            return redirect('index')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
