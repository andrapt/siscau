from django.db import migrations


def criar_perfis_base(apps, schema_editor):
    Sistema = apps.get_model('usuarios', 'Sistema')
    Perfil = apps.get_model('usuarios', 'Perfil')

    sistema, _ = Sistema.objects.get_or_create(
        nome='SISCAU',
        defaults={
            'descricao': 'Sistema principal de acesso ao SISCAU',
            'ativo': True,
        },
    )

    perfis = {
        'Administrador': 'Perfil com permissão para cadastrar e administrar usuários.',
        'Produtor': 'Perfil padrão do produtor para operar o sistema.',
    }

    for nome, descricao in perfis.items():
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


def remover_perfis_base(apps, schema_editor):
    Perfil = apps.get_model('usuarios', 'Perfil')
    Sistema = apps.get_model('usuarios', 'Sistema')

    try:
        sistema = Sistema.objects.get(nome='SISCAU')
    except Sistema.DoesNotExist:
        return

    Perfil.objects.filter(
        sistema=sistema,
        nome__in=['Administrador', 'Produtor'],
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_perfis_base, remover_perfis_base),
    ]
