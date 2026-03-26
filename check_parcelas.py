import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siscau.settings')
django.setup()

from fazenda.models import Financiamento, ParcelaFinanciamento

print('=== VERIFICAÇÃO DE PARCELAS ===')
print(f'Total de Financiamentos: {Financiamento.objects.count()}')
print(f'Total de Parcelas: {ParcelaFinanciamento.objects.count()}')
print()

print('Parcelas por financiamento:')
for f in Financiamento.objects.all():
    parcelas_count = f.parcelafinanciamento_set.count()
    print(f'  {f.item}: {parcelas_count} parcelas')
    
    if parcelas_count > 0:
        print('    Parcelas:')
        for p in f.parcelafinanciamento_set.all()[:3]:  # Mostrar apenas as 3 primeiras
            print(f'      - Parcela {p.numero_parcela}: R$ {p.valor_parcela} - {p.status}')
        if parcelas_count > 3:
            print(f'      ... e mais {parcelas_count - 3} parcelas')
    print()