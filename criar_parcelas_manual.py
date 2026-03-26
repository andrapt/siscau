import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siscau.settings')
django.setup()

from fazenda.models import Financiamento, ParcelaFinanciamento

print('=== CRIANDO PARCELAS MANUALMENTE ===')

# Buscar o financiamento existente
financiamento = Financiamento.objects.first()

if financiamento:
    print(f'Financiamento encontrado: {financiamento.item}')
    print(f'Número de parcelas: {financiamento.numero_parcelas}')
    print(f'Valor financiado: {financiamento.valor_financiado}')
    print(f'Data primeira parcela: {financiamento.data_vencimento_primeira}')
    
    # Verificar se já existem parcelas
    parcelas_existentes = financiamento.parcelafinanciamento_set.count()
    print(f'Parcelas existentes: {parcelas_existentes}')
    
    if parcelas_existentes == 0:
        print('Criando parcelas...')
        try:
            financiamento.criar_parcelas()
            print('Parcelas criadas com sucesso!')
            
            # Verificar se foram criadas
            parcelas_criadas = financiamento.parcelafinanciamento_set.count()
            print(f'Total de parcelas criadas: {parcelas_criadas}')
            
            # Mostrar algumas parcelas
            for p in financiamento.parcelafinanciamento_set.all()[:3]:
                print(f'  - Parcela {p.numero_parcela}: R$ {p.valor_parcela:.2f} - Vencimento: {p.data_vencimento}')
                
        except Exception as e:
            print(f'Erro ao criar parcelas: {e}')
    else:
        print('Financiamento já possui parcelas.')
else:
    print('Nenhum financiamento encontrado.')