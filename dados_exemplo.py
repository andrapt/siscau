from django.utils import timezone
from datetime import datetime, timedelta
from fazenda.models import Fazenda, Categoria, Despesa, Variedade, Cultura, TipoColheita, Quadra, Colheita
import random

# Criar fazenda se não existir
try:
    fazenda = Fazenda.objects.get(id=1)
except Fazenda.DoesNotExist:
    fazenda = Fazenda.objects.create(
        nome="Fazenda Modelo",
        localizacao="Rodovia BR 101, Km 123, Ilhéus-BA",
        area=150.00
    )
    print("Fazenda criada com sucesso!")

# Criar categorias de despesas
categorias = [
    "Energia",
    "Combustível",
    "Mão de obra",
    "Insumos",
    "Manutenção",
    "Transporte"
]

for cat in categorias:
    try:
        Categoria.objects.get(nome=cat)
    except Categoria.DoesNotExist:
        Categoria.objects.create(nome=cat)
        print(f"Categoria {cat} criada com sucesso!")

# Criar variedades
variedades = [
    {"nome": "Cacau CCN-51", "descricao": "Variedade de alta produtividade"},
    {"nome": "Cacau Catongo", "descricao": "Variedade de frutos brancos"},
    {"nome": "Cacau Comum", "descricao": "Variedade tradicional da região"}
]

for var in variedades:
    try:
        Variedade.objects.get(nome=var["nome"])
    except Variedade.DoesNotExist:
        Variedade.objects.create(nome=var["nome"], descricao=var["descricao"])
        print(f"Variedade {var['nome']} criada com sucesso!")

# Criar culturas
culturas = [
    {"nome": "Cacau", "descricao": "Cultura principal"},
    {"nome": "Banana", "descricao": "Cultura de sombreamento"},
    {"nome": "Açaí", "descricao": "Cultura complementar"}
]

for cult in culturas:
    try:
        Cultura.objects.get(nome=cult["nome"])
    except Cultura.DoesNotExist:
        Cultura.objects.create(nome=cult["nome"], descricao=cult["descricao"])
        print(f"Cultura {cult['nome']} criada com sucesso!")

# Criar tipos de colheita
tipos_colheita = ["Integral", "Meia safra", "Temporão"]

for tipo in tipos_colheita:
    try:
        TipoColheita.objects.get(nome=tipo)
    except TipoColheita.DoesNotExist:
        TipoColheita.objects.create(nome=tipo)
        print(f"Tipo de colheita {tipo} criado com sucesso!")

# Criar quadras
quadras = [
    {"nome": "Quadra A", "area": 25.5, "tipoSolo": "Argiloso"},
    {"nome": "Quadra B", "area": 30.0, "tipoSolo": "Arenoso"},
    {"nome": "Quadra C", "area": 20.0, "tipoSolo": "Misto"}
]

for q in quadras:
    try:
        Quadra.objects.get(nome=q["nome"])
    except Quadra.DoesNotExist:
        quadra = Quadra.objects.create(
            fazenda=fazenda,
            nome=q["nome"],
            area=q["area"],
            tipoSolo=q["tipoSolo"],
            dataPlantio=timezone.now() - timedelta(days=random.randint(365, 1825)),
            espacamento="3x3m"
        )
        # Adicionar variedades e culturas às quadras
        for v in Variedade.objects.all():
            if random.choice([True, False]):
                quadra.variedades.add(v)
        
        for c in Cultura.objects.all():
            if random.choice([True, False]):
                quadra.culturas.add(c)
                
        print(f"Quadra {q['nome']} criada com sucesso!")

# Criar despesas para o ano atual
ano_atual = datetime.now().year
categorias_obj = list(Categoria.objects.all())

# Limpar despesas existentes para evitar duplicação
Despesa.objects.filter(data__year=ano_atual).delete()

# Criar despesas para cada mês do ano atual
for mes in range(1, 13):
    # Número aleatório de despesas por mês (2 a 5)
    num_despesas = random.randint(2, 5)
    
    for _ in range(num_despesas):
        # Data aleatória dentro do mês
        if mes <= datetime.now().month:
            dia = random.randint(1, 28)
            data = datetime(ano_atual, mes, dia)
            
            # Categoria aleatória
            categoria = random.choice(categorias_obj)
            
            # Valor aleatório entre R$ 100 e R$ 2000
            valor = round(random.uniform(100, 2000), 2)
            
            Despesa.objects.create(
                fazenda=fazenda,
                categoria=categoria,
                data=data,
                descricao=f"Despesa com {categoria.nome.lower()}",
                valor=valor
            )
            print(f"Despesa de R$ {valor} criada para {data.strftime('%d/%m/%Y')}")

# Criar colheitas para o ano atual
variedades_obj = list(Variedade.objects.all())
quadras_obj = list(Quadra.objects.all())
tipos_colheita_obj = list(TipoColheita.objects.all())

# Limpar colheitas existentes para evitar duplicação
Colheita.objects.filter(data__year=ano_atual).delete()

# Criar colheitas para cada mês do ano atual (exceto meses futuros)
for mes in range(1, 13):
    if mes <= datetime.now().month:
        # Número aleatório de colheitas por mês (1 a 3)
        num_colheitas = random.randint(1, 3)
        
        for _ in range(num_colheitas):
            # Data aleatória dentro do mês
            dia = random.randint(1, 28)
            data = datetime(ano_atual, mes, dia)
            
            # Quadra e variedade aleatórias
            quadra = random.choice(quadras_obj)
            variedade = random.choice(variedades_obj)
            tipo_colheita = random.choice(tipos_colheita_obj)
            
            # Peso aleatório entre 50 e 200 arrobas
            peso = round(random.uniform(50, 200), 2)
            
            # Preço aleatório entre R$ 150 e R$ 250 por arroba
            preco = round(random.uniform(150, 250), 2)
            
            # Valor total
            valor_total = round(peso * preco, 2)
            
            Colheita.objects.create(
                data=data,
                ano=ano_atual,
                peso=peso,
                preco=preco,
                valorTotal=valor_total,
                descricao=f"Colheita de {variedade.nome}",
                quadra=quadra,
                variedade=variedade,
                tipoColheita=tipo_colheita
            )
            print(f"Colheita de {peso} arrobas criada para {data.strftime('%d/%m/%Y')}")

print("\nDados de exemplo criados com sucesso!")