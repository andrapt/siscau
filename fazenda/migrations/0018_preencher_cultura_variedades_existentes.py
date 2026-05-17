from django.db import migrations


def preencher_cultura_variedades_existentes(apps, schema_editor):
    Cultura = apps.get_model('fazenda', 'Cultura')
    Variedade = apps.get_model('fazenda', 'Variedade')

    culturas = list(Cultura.objects.all())
    for variedade in Variedade.objects.filter(cultura__isnull=True):
        nome_variedade = (variedade.nome or '').strip().lower()
        for cultura in culturas:
            nome_cultura = (cultura.nome or '').strip().lower()
            if nome_cultura and nome_cultura in nome_variedade:
                variedade.cultura_id = cultura.id
                variedade.save(update_fields=['cultura'])
                break


class Migration(migrations.Migration):

    dependencies = [
        ('fazenda', '0017_remove_colheita_preco_remove_colheita_valortotal_and_more'),
    ]

    operations = [
        migrations.RunPython(preencher_cultura_variedades_existentes, migrations.RunPython.noop),
    ]
