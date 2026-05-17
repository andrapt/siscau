from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Min
from datetime import date
import locale
from .models import Cultura, Variedade, Insumo, TipoInsumo, Fazenda, TipoAtividade, Quadra, Categoria, TipoColheita, Despesa, Colheita, Manejo, CalendarioAgricola, Financiamento, ParcelaFinanciamento
from .forms import CulturaForm, VariedadeForm, InsumoForm, TipoInsumoForm, TipoAtividadeForm, QuadraForm, CategoriaForm, TipoColheitaForm, DespesaForm, ColheitaForm, ManejoForm, CalendarioAgricolaForm, FinanciamentoForm, ParcelaFinanciamentoForm
# import locale
# Página inicial do sistema
@login_required
def index(request):
    import datetime
    
    # Seleção de ano via querystring (?ano=YYYY) com fallback para ano corrente
    ano_param = request.GET.get('ano')
    ano_corrente = datetime.datetime.now().year
    try:
        ano_atual = int(ano_param) if ano_param else ano_corrente
    except (TypeError, ValueError):
        ano_atual = ano_corrente
    
    # Busca os dados da Fazenda na base de dados
    try:
        fazenda = Fazenda.objects.get(id=1)
    except Fazenda.DoesNotExist:
        fazenda = None
    
    # Calcula o total de despesas do ano atual (evita carregar todas as colunas)
    despesas_ano_qs = Despesa.objects.filter(data__year=ano_atual)
    total_despesas = despesas_ano_qs.aggregate(total=Sum('valor'))['total'] or 0
    
    # A colheita nao registra mais dados financeiros.
    colheitas_ano = Colheita.objects.filter(data__year=ano_atual)
    total_receitas = 0
    
    # Calcula o saldo total
    total_geral = total_receitas - total_despesas
    
    # Calcula o total de arrobas colhidas no ano atual
    total_arrobas = sum(colheita.peso for colheita in colheitas_ano)/15
    
    # Dados para o gráfico de despesas x receitas por mês
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    dados_despesas = [0] * 12
    dados_receitas = [0] * 12
    
    # Agrupa despesas por mês com select limitado
    for data_despesa, valor in despesas_ano_qs.values_list('data', 'valor'):
        if data_despesa:
            mes = data_despesa.month - 1  # Ajusta para índice 0-11
            dados_despesas[mes] += float(valor)
    
    # Despesas por categoria (ano corrente)
    despesas_por_categoria_qs = (
        Despesa.objects
        .filter(data__year=ano_atual)
        .values('categoria__nome')
        .annotate(total=Sum('valor'))
        .order_by('categoria__nome')
    )
    despesas_categoria_labels = [item['categoria__nome'] for item in despesas_por_categoria_qs]
    despesas_categoria_valores = [float(item['total']) for item in despesas_por_categoria_qs]

    # Despesas por fonte (ano corrente)
    despesas_por_fonte_qs = (
        Despesa.objects
        .filter(data__year=ano_atual)
        .values('fonte')
        .annotate(total=Sum('valor'))
        .order_by('fonte')
    )
    fonte_field = Despesa._meta.get_field('fonte')
    fonte_choices = dict(fonte_field.choices) if hasattr(fonte_field, 'choices') else {}
    def _label_fonte(value):
        if value in fonte_choices:
            return fonte_choices[value]
        if value is None:
            return 'Sem Fonte'
        return str(value)
    despesas_fonte_labels = [_label_fonte(item['fonte']) for item in despesas_por_fonte_qs]
    despesas_fonte_valores = [float(item['total']) for item in despesas_por_fonte_qs]

    # Busca atividades do calendário agrícola para o mês atual
    mes_atual = datetime.datetime.now().month
    meses_nomes = {
        1: 'janeiro', 2: 'fevereiro', 3: 'marco', 4: 'abril',
        5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
        9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
    }
    nome_mes_atual = meses_nomes.get(mes_atual, '')
    
    # Busca atividades do calendário para o mês atual
    atividades_mes_atual = CalendarioAgricola.objects.filter(mes=nome_mes_atual)

    # Busca financiamentos ativos para exibir no widget
    financiamentos_ativos = Financiamento.objects.filter(status='ativo').order_by('-data_inicio')[:6]  # Limita a 6 para não sobrecarregar a tela
    
    # A propriedade percentual_pendente já está definida no modelo

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    # Construir lista de anos disponíveis (dinâmico, baseado em dados existentes)
    min_despesa_data = Despesa.objects.aggregate(m=Min('data'))['m']
    min_colheita_data = Colheita.objects.aggregate(m=Min('data'))['m']
    datas_validas = [d for d in [min_despesa_data, min_colheita_data] if d]
    if datas_validas:
        min_ano = min(datas_validas).year
    else:
        # Fallback para últimos 20 anos quando não há dados
        min_ano = ano_corrente - 20
    # Garantir um limite inferior razoável
    if min_ano < 1900:
        min_ano = 1900
    anos_disponiveis = list(range(ano_corrente, min_ano - 1, -1))
     
    context = {
        "fazenda": fazenda,
        "total_despesas": locale.currency(total_despesas, grouping=True, symbol=None),
        "total_receitas": locale.currency(total_receitas, grouping=True, symbol=None),
        "total_despesas_grafico": str(total_despesas).replace(",", "."),
        "total_receitas_grafico": str(total_receitas).replace(",", "."),
        "total_arrobas": total_arrobas,
        "meses": meses,
        "dados_despesas": dados_despesas,
        "dados_receitas": dados_receitas,
        "despesas_categoria_labels": despesas_categoria_labels,
        "despesas_categoria_valores": despesas_categoria_valores,
        "despesas_fonte_labels": despesas_fonte_labels,
        "despesas_fonte_valores": despesas_fonte_valores,
        "ano_atual": ano_atual,
        "total_geral": total_geral,
        "atividades_mes_atual": atividades_mes_atual,
        "nome_mes_atual": nome_mes_atual.title(),
        "financiamentos_ativos": financiamentos_ativos
    }
    # Adicionar anos disponíveis ao contexto para seletor
    context["anos_disponiveis"] = anos_disponiveis
    
    return render(request, "index.html", context)





#
# Métodod para gerenciamento de Cultura #############################################
#
@login_required
def listaCulturas (request):

    # busca do request a informação de pesquisa caso o usuário tenha feito
    pesquisa = request.GET.get("search")
    
    """ 
        Lista todas a Culturas cadastradas no sistema
    """
    if pesquisa:
        culturas = Cultura.objects.filter(nome__icontains=pesquisa)
    else:
        culturas = Cultura.objects.all().order_by('nome')

    # Procedimentos para paginação
    paginator = Paginator(culturas, 10)  # 2 culturas por página
    pagina = request.GET.get('page')
    culturas = paginator.get_page(pagina)   

    context = {"culturas": culturas}
    
    return render(request, "lista_culturas.html", {"culturas": culturas})

def editarCultura(request, id):
    cultura = get_object_or_404(Cultura,id=id)
    if request.method == "POST":
        form = CulturaForm(request.POST, instance=cultura)
        if form.is_valid():
            form.save()
            messages.success(request, "Cultura atualizada com sucesso!")
            return redirect('culturas')
    else:

        form = CulturaForm(instance=cultura)

    return render(request, "gerencia_cultura.html", {"form": form, 'editar':True})

def cadastrarCultura(request):
    if request.method == "POST":
        form = CulturaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cultura cadastrada com sucesso!")
            return redirect('culturas')
    else:
        form = CulturaForm()

    return render(request, "gerencia_cultura.html", {"form": form})

def excluirCultura(request, id):
    cultura = get_object_or_404(Cultura, id=id)
    cultura.delete()
    messages.success(request, "Cultura excluída com sucesso!")
    return redirect('culturas')





#
# Métodod para gerenciamento de Variedade de Cultura #############################################
#
@login_required
def listaVariedades (request):

    # busca do request a informação de pesquisa caso o usuário tenha feito
    pesquisa = request.GET.get("search")
    
    """ 
        Lista todas a Variedades cadastradas no sistema
    """
    if pesquisa:
        variedades = Variedade.objects.filter(nome__icontains=pesquisa)
    else:
        variedades = Variedade.objects.all().order_by('nome')

    # Procedimentos para paginação
    paginator = Paginator(variedades, 10)  # 2 variedades por página
    pagina = request.GET.get('page')
    variedades = paginator.get_page(pagina)   

    context = {"variedades": variedades}
    
    return render(request, "lista_variedades.html", {"variedades": variedades})

def editarVariedade(request, id):
    variedade = get_object_or_404(Variedade,id=id)
    if request.method == "POST":
        form = VariedadeForm(request.POST, instance=variedade)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro atualizada com sucesso!")
            return redirect('variedades')
    else:
        form = VariedadeForm(instance=variedade)

    return render(request, "gerencia_variedade.html", {"form": form, 'editar':True})

def cadastrarVariedade(request):
    if request.method == "POST":
        form = VariedadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro cadastrado com sucesso!")
            return redirect('variedades')
    else:
        form = VariedadeForm()

    return render(request, "gerencia_variedade.html", {"form": form})

def excluirVariedade(request, id):
    variedade = get_object_or_404(Variedade, id=id)
    variedade.delete()
    messages.success(request, "Registro excluído com sucesso!")
    return redirect('variedades')





#
# Métodod para gerenciamento de Insumos #############################################
#
@login_required
def listaInsumos (request):

    # busca do request a informação de pesquisa caso o usuário tenha feito
    pesquisa = request.GET.get("search")
    
    """ 
        Lista todas os Insumos cadastradas no sistema
    """
    if pesquisa:
        insumos = Insumo.objects.filter(nome__icontains=pesquisa)
    else:
        insumos = Insumo.objects.all().order_by('nome')

    # Procedimentos para paginação
    paginator = Paginator(insumos, 10)  # 2 insumos por página
    pagina = request.GET.get('page')
    insumos = paginator.get_page(pagina)   

    context = {"insumos": insumos}
    
    return render(request, "insumo/lista_insumos.html", {"insumos": insumos})

def editarInsumo(request, id):
    insumo = get_object_or_404(Insumo,id=id)
    if request.method == "POST":
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro atualizada com sucesso!")
            return redirect('insumos')
    else:
        form = InsumoForm(instance=insumo)

    return render(request, "insumo/gerencia_insumo.html", {"form": form, 'editar':True})

def cadastrarInsumo(request):
    if request.method == "POST":
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro cadastrado com sucesso!")
            return redirect('insumos')
    else:
        form = InsumoForm()

    return render(request, "insumo/gerencia_insumo.html", {"form": form})

def excluirInsumo(request, id):
    insumo = get_object_or_404(Insumo, id=id)
    insumo.delete()
    messages.success(request, "Registro excluído com sucesso!")
    return redirect('insumos')





#
# Métodod para gerenciamento de Tipo de Insumos #############################################
#
@login_required
def listaTipoInsumos (request):

    # busca do request a informação de pesquisa caso o usuário tenha feito
    pesquisa = request.GET.get("search")
    
    """ 
        Lista todas os Tipo de Insumos cadastradas no sistema
    """
    if pesquisa:
        tipoInsumos = TipoInsumo.objects.filter(nome__icontains=pesquisa)
    else:
        tipoInsumos = TipoInsumo.objects.all().order_by('nome')

    # Procedimentos para paginação
    paginator = Paginator(tipoInsumos, 10)  # 2 insumos por página
    pagina = request.GET.get('page')
    tipoInsumos = paginator.get_page(pagina)   

    context = {"tipoInsumos": tipoInsumos}
    
    return render(request, "insumo/lista_tipo_insumos.html", context)

def editarTipoInsumo(request, id):
    tipoInsumo = get_object_or_404(TipoInsumo,id=id)
    if request.method == "POST":
        form = TipoInsumoForm(request.POST, instance=tipoInsumo)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro atualizada com sucesso!")
            return redirect('tipo_insumos')
    else:
        form = TipoInsumoForm(instance=tipoInsumo)

    return render(request, "insumo/gerencia_tipo_insumo.html", {"form": form, 'editar':True})

def cadastrarTipoInsumo(request):
    if request.method == "POST":
        form = TipoInsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro cadastrado com sucesso!")
            return redirect('tipo_insumos')
    else:
        form = TipoInsumoForm()

    return render(request, "insumo/gerencia_tipo_insumo.html", {"form": form})

def excluirTipoInsumo(request, id):
    tipoInsumo = get_object_or_404(TipoInsumo, id=id)
    tipoInsumo.delete()
    messages.success(request, "Registro excluído com sucesso!")
    return redirect('tipo_insumos')





#
# Métodod para gerenciamento de Tipo de Atividade #############################################
#
@login_required
def listaTipoAtividades(request):

    # busca do request a informação de pesquisa caso o usuário tenha feito
    pesquisa = request.GET.get("search")
    
    """ 
        Lista todas os Tipo de Atividade cadastradas no sistema
    """
    if pesquisa:
        tipoAtividades = TipoAtividade.objects.filter(nome__icontains=pesquisa)
    else:
        tipoAtividades = TipoAtividade.objects.all().order_by('nome')

    # Procedimentos para paginação
    paginator = Paginator(tipoAtividades, 10)  # 2 atividades por página
    pagina = request.GET.get('page')
    tipoAtividades = paginator.get_page(pagina)   

    context = {"tipoAtividades": tipoAtividades}
    
    return render(request, "manejo/lista_tipo_atividades.html", context)

def editarTipoAtividade(request, id):
    tipoAtividade = get_object_or_404(TipoAtividade,id=id)
    if request.method == "POST":
        form = TipoAtividadeForm(request.POST, instance=tipoAtividade)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro atualizada com sucesso!")
            return redirect('tipo_atividades')
    else:
        form = TipoAtividadeForm(instance=tipoAtividade)

    return render(request, "manejo/gerencia_tipo_atividade.html", {"form": form, 'editar':True})

def cadastrarTipoAtividade(request):
    if request.method == "POST":
        form = TipoAtividadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro cadastrado com sucesso!")
            return redirect('tipo_atividades')
    else:
        form = TipoAtividadeForm()

    return render(request, "manejo/gerencia_tipo_atividade.html", {"form": form})

def excluirTipoAtividade(request, id):
    tipoAtividade = get_object_or_404(TipoAtividade, id=id)
    tipoAtividade.delete()
    messages.success(request, "Registro excluído com sucesso!")
    return redirect('tipo_atividades')





#
# Métodod para gerenciamento de Tipo de Quadra #############################################
#
@login_required
def listaQuadras(request):

    # busca do request a informação de pesquisa caso o usuário tenha feito
    pesquisa = request.GET.get("search")
    
    """ 
        Lista todas Quadras cadastradas no sistema
    """
    if pesquisa:
        quadras = Quadra.objects.filter(nome__icontains=pesquisa)
    else:
        quadras = Quadra.objects.all().order_by('nome')

    # Procedimentos para paginação
    paginator = Paginator(quadras, 10)  # 2 Quadras por página
    pagina = request.GET.get('page')
    quadras = paginator.get_page(pagina)   

    context = {"quadras": quadras}
    
    return render(request, "quadra/lista_quadra.html", context)

def editarQuadra(request, id):
    quadra = get_object_or_404(Quadra,id=id)
    if request.method == "POST":
        form = QuadraForm(request.POST, instance=quadra)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro atualizada com sucesso!")
            return redirect('quadras')
    else:
        form = QuadraForm(instance=quadra)

    return render(request, "quadra/gerencia_quadra.html", {"form": form, 'editar':True})

def cadastrarQuadra(request):
    if request.method == "POST":
        form = QuadraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro cadastrado com sucesso!")
            return redirect('quadras')
    else:
        form = QuadraForm()

    return render(request, "quadra/gerencia_quadra.html", {"form": form})

def excluirQuadra(request, id):
    quadra = get_object_or_404(Quadra, id=id)
    quadra.delete()
    messages.success(request, "Registro excluído com sucesso!")
    return redirect('quadras')





#
# Métodod para gerenciamento de Categoria de Despesa #############################################
#
@login_required
def listaCategorias(request):

    # busca do request a informação de pesquisa caso o usuário tenha feito
    pesquisa = request.GET.get("search")
    
    """ 
        Lista todas as categorias de despesas cadastradas no sistema
    """
    if pesquisa:
        categorias = Categoria.objects.filter(nome__icontains=pesquisa)
    else:
        categorias = Categoria.objects.all().order_by('nome')

    # Procedimentos para paginação
    paginator = Paginator(categorias, 10)  # 2 categorias por página
    pagina = request.GET.get('page')
    categorias = paginator.get_page(pagina)   

    context = {"categorias": categorias}
    
    return render(request, "despesa/lista_categoria.html", context)

def editarCategoria(request, id):
    categoria = get_object_or_404(Categoria,id=id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro atualizada com sucesso!")
            return redirect('categorias')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, "despesa/gerencia_categoria.html", {"form": form, 'editar':True})

def cadastrarCategoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro cadastrado com sucesso!")
            return redirect('categorias')
    else:
        form = CategoriaForm()

    return render(request, "despesa/gerencia_categoria.html", {"form": form})

def excluirCategoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    messages.success(request, "Registro excluído com sucesso!")
    return redirect('categorias')





#
# Métodod para gerenciamento de Tipo de Colheita #############################################
#
@login_required
def listaTipoColheitas(request):

    # busca do request a informação de pesquisa caso o usuário tenha feito
    pesquisa = request.GET.get("search")
    
    """ 
        Lista todas os Tipo de Colheita cadastradas no sistema
    """
    if pesquisa:
        tipoColheitas = TipoColheita.objects.filter(nome__icontains=pesquisa)
    else:
        tipoColheitas = TipoColheita.objects.all().order_by('nome')

    # Procedimentos para paginação
    paginator = Paginator(tipoColheitas, 10)  # 2 tipos de colheita por página
    pagina = request.GET.get('page')
    tipoColheitas = paginator.get_page(pagina)   

    context = {"tipoColheitas": tipoColheitas}
    
    return render(request, "colheita/lista_tipo_colheita.html", context)

def editarTipoColheita(request, id):
    tipoColheita = get_object_or_404(TipoColheita,id=id)
    if request.method == "POST":
        form = TipoColheitaForm(request.POST, instance=tipoColheita)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro atualizada com sucesso!")
            return redirect('tipo_colheitas')
    else:
        form = TipoColheitaForm(instance=tipoColheita)

    return render(request, "colheita/gerencia_tipo_colheita.html", {"form": form, 'editar':True})

def cadastrarTipoColheita(request):
    if request.method == "POST":
        form = TipoColheitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro cadastrado com sucesso!")
            return redirect('tipo_colheitas')
    else:
        form = TipoColheitaForm()

    return render(request, "colheita/gerencia_tipo_colheita.html", {"form": form})

def excluirTipoColheita(request, id):
    tipoColheita = get_object_or_404(TipoColheita, id=id)
    tipoColheita.delete()
    messages.success(request, "Registro excluído com sucesso!")
    return redirect('tipo_colheitas')





#
# Métodod para gerenciamento de Despesa de Despesa #############################################
#
@login_required
def listaDespesas(request):

    # busca do request a informação de pesquisa caso o usuário tenha feito
    pesquisa = request.GET.get("search")
    
    """ 
        Lista todas as despesas cadastradas no sistema
    """
    if pesquisa:
        despesas = Despesa.objects.filter(descricao__icontains=pesquisa).order_by('-data')
    else:
        despesas = Despesa.objects.all().order_by('-data')

    # Procedimentos para paginação
    paginator = Paginator(despesas, 10)  # 2 despesas por página
    pagina = request.GET.get('page')
    despesas = paginator.get_page(pagina)   

    context = {"despesas": despesas}
    
    return render(request, "despesa/lista_despesa.html", context)

def editarDespesa(request, id):
    despesa = get_object_or_404(Despesa, id=id)
    if request.method == "POST":
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro atualizada com sucesso!")
            return redirect('despesas')
    else:
        form = DespesaForm(instance=despesa)

    return render(request, "despesa/gerencia_despesa.html", {"form": form, 'editar':True})

def cadastrarDespesa(request):
    if request.method == "POST":
        form = DespesaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro cadastrado com sucesso!")
            return redirect('despesas')
    else:
        form = DespesaForm()

    return render(request, "despesa/gerencia_despesa.html", {"form": form})

def excluirDespesa(request, id):
    despesa = get_object_or_404(Despesa, id=id)
    despesa.delete()
    messages.success(request, "Registro excluído com sucesso!")
    return redirect('despesas')




#
# Métodos para gerenciamento de Colheitas #############################################
#
@login_required
def listaColheitas(request):
    ano_corrente = date.today().year
    pesquisa = request.GET.get("search", "").strip()
    ano_param = request.GET.get("ano")

    try:
        ano_selecionado = int(ano_param) if ano_param else ano_corrente
    except (TypeError, ValueError):
        ano_selecionado = ano_corrente

    """
        Lista as Colheitas cadastradas no sistema.
        Por padrão, exibe apenas o ano corrente e permite consultar outros anos.
    """
    colheitas = Colheita.objects.filter(ano=ano_selecionado)

    if pesquisa:
        colheitas = colheitas.filter(
            Q(quadra__nome__icontains=pesquisa) |
            Q(variedade__nome__icontains=pesquisa)
        )

    resumo_geral_query = (
        colheitas.values('cultura__nome', 'situacao_vassoura_bruxa')
        .annotate(total_peso=Sum('peso'))
        .order_by('cultura__nome', 'situacao_vassoura_bruxa')
    )

    resumo_geral_map = {}
    for item in resumo_geral_query:
        cultura_nome = item['cultura__nome'] or 'Sem cultura'
        total_peso = item['total_peso'] or 0
        eh_cacau = 'cacau' in cultura_nome.lower()

        if cultura_nome not in resumo_geral_map:
            resumo_geral_map[cultura_nome] = {
                'cultura_nome': cultura_nome,
                'total_peso': 0,
                'total_arrobas': 0,
                'eh_cacau': eh_cacau,
                'com_vassoura_peso': 0,
                'com_vassoura_arrobas': 0,
                'sem_vassoura_peso': 0,
                'sem_vassoura_arrobas': 0,
                'nao_informado_peso': 0,
                'nao_informado_arrobas': 0,
            }

        resumo_geral_map[cultura_nome]['total_peso'] += total_peso
        if eh_cacau:
            resumo_geral_map[cultura_nome]['total_arrobas'] += total_peso / 15
            situacao = item['situacao_vassoura_bruxa'] or ''
            if situacao == 'COM':
                resumo_geral_map[cultura_nome]['com_vassoura_peso'] += total_peso
                resumo_geral_map[cultura_nome]['com_vassoura_arrobas'] += total_peso / 15
            elif situacao == 'SEM':
                resumo_geral_map[cultura_nome]['sem_vassoura_peso'] += total_peso
                resumo_geral_map[cultura_nome]['sem_vassoura_arrobas'] += total_peso / 15
            else:
                resumo_geral_map[cultura_nome]['nao_informado_peso'] += total_peso
                resumo_geral_map[cultura_nome]['nao_informado_arrobas'] += total_peso / 15

    resumo_geral_culturas = list(resumo_geral_map.values())

    resumo_por_quadra_query = (
        colheitas.values(
            'quadra_id',
            'quadra__nome',
            'cultura__nome',
            'situacao_vassoura_bruxa',
        )
        .annotate(total_peso=Sum('peso'))
        .order_by('quadra__nome', 'cultura__nome', 'situacao_vassoura_bruxa')
    )

    cards_quadras = []
    card_atual = None
    quadra_atual_id = None

    for item in resumo_por_quadra_query:
        if item['quadra_id'] != quadra_atual_id:
            card_atual = {
                'quadra_nome': item['quadra__nome'],
                'culturas': [],
                'tem_cacau': False,
            }
            cards_quadras.append(card_atual)
            quadra_atual_id = item['quadra_id']

        cultura_nome = item['cultura__nome'] or 'Sem cultura'
        total_peso = item['total_peso'] or 0
        eh_cacau = 'cacau' in cultura_nome.lower()
        situacao_vassoura = item['situacao_vassoura_bruxa'] or ''
        badge_class = 'badge-secondary'
        situacao_label = None

        if eh_cacau:
            card_atual['tem_cacau'] = True
            if situacao_vassoura == 'COM':
                badge_class = 'badge-danger'
                situacao_label = 'Com vassoura de bruxa'
            elif situacao_vassoura == 'SEM':
                badge_class = 'badge-success'
                situacao_label = 'Sem vassoura de bruxa'
            else:
                badge_class = 'badge-warning'
                situacao_label = 'Situação não informada'

        card_atual['culturas'].append({
            'cultura_nome': cultura_nome,
            'total_peso': total_peso,
            'total_arrobas': total_peso / 15 if eh_cacau else None,
            'eh_cacau': eh_cacau,
            'situacao_label': situacao_label,
            'badge_class': badge_class,
        })

    colheitas = colheitas.order_by('-data', '-id')

    anos_disponiveis = list(
        Colheita.objects.order_by('-ano').values_list('ano', flat=True).distinct()
    )
    if ano_corrente not in anos_disponiveis:
        anos_disponiveis.insert(0, ano_corrente)

    # Procedimentos para paginação
    paginator = Paginator(colheitas, 10)  # 10 colheitas por página
    pagina = request.GET.get('page')
    colheitas = paginator.get_page(pagina)   

    context = {
        "colheitas": colheitas,
        "search": pesquisa,
        "ano_selecionado": ano_selecionado,
        "anos_disponiveis": anos_disponiveis,
        "resumo_geral_culturas": resumo_geral_culturas,
        "cards_quadras": cards_quadras,
    }
    
    return render(request, "colheita/lista_colheitas.html", context)


def _colheita_contexto_formulario(form, editar=False):
    variedades_data = [
        {
            "id": variedade.id,
            "nome": variedade.nome,
            "cultura_id": variedade.cultura_id,
        }
        for variedade in Variedade.objects.select_related('cultura').order_by('nome')
    ]
    return {
        "form": form,
        "editar": editar,
        "variedades_data": variedades_data,
    }

def editarColheita(request, id):
    colheita = get_object_or_404(Colheita, id=id)
    if request.method == "POST":
        form = ColheitaForm(request.POST, instance=colheita)
        if form.is_valid():
            form.save()
            messages.success(request, "Colheita atualizada com sucesso!")
            return redirect('colheitas')
    else:
        form = ColheitaForm(instance=colheita)

    return render(request, "colheita/gerencia_colheita.html", _colheita_contexto_formulario(form, editar=True))

def cadastrarColheita(request):
    if request.method == "POST":
        form = ColheitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Colheita cadastrada com sucesso!")
            return redirect('colheitas')
    else:
        form = ColheitaForm()

    return render(request, "colheita/gerencia_colheita.html", _colheita_contexto_formulario(form))

def excluirColheita(request, id):
    colheita = get_object_or_404(Colheita, id=id)
    colheita.delete()
    messages.success(request, "Colheita excluída com sucesso!")
    return redirect('colheitas')




#
# Métodos para gerenciamento de Manejos #############################################
#
@login_required
def listaManejos(request):

    # busca do request a informação de pesquisa caso o usuário tenha feito
    pesquisa = request.GET.get("search")
    
    """ 
        Lista todos os Manejos cadastrados no sistema
    """
    if pesquisa:
        manejos = Manejo.objects.filter(quadra__nome__icontains=pesquisa) | Manejo.objects.filter(responsavel__icontains=pesquisa) | Manejo.objects.filter(tipoAtividade__nome__icontains=pesquisa)
    else:
        manejos = Manejo.objects.all().order_by('-dataInicio')

    # Procedimentos para paginação
    paginator = Paginator(manejos, 10)  # 10 manejos por página
    pagina = request.GET.get('page')
    manejos = paginator.get_page(pagina)   

    context = {"manejos": manejos}
    
    return render(request, "manejo/lista_manejos.html", context)

def editarManejo(request, id):
    manejo = get_object_or_404(Manejo, id=id)
    if request.method == "POST":
        form = ManejoForm(request.POST, instance=manejo)
        if form.is_valid():
            form.save()
            messages.success(request, "Manejo atualizado com sucesso!")
            return redirect('manejos')
    else:
        form = ManejoForm(instance=manejo)

    return render(request, "manejo/gerencia_manejo.html", {"form": form, 'editar':True})

def cadastrarManejo(request):
    if request.method == "POST":
        form = ManejoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Manejo cadastrado com sucesso!")
            return redirect('manejos')
    else:
        form = ManejoForm()

    return render(request, "manejo/gerencia_manejo.html", {"form": form})

def excluirManejo(request, id):
    manejo = get_object_or_404(Manejo, id=id)
    manejo.delete()
    messages.success(request, "Manejo excluído com sucesso!")
    return redirect('manejos')

# Views para Calendário Agrícola
@login_required
def listaCalendarios(request):
    pesquisa = request.GET.get('pesquisa')
    """ 
        Lista todos os Calendários Agrícolas cadastrados no sistema
    """
    if pesquisa:
        calendarios = CalendarioAgricola.objects.filter(cultura__nome__icontains=pesquisa) | CalendarioAgricola.objects.filter(mes__icontains=pesquisa)
    else:
        calendarios = CalendarioAgricola.objects.all().order_by('cultura__nome', 'mes')

    # Procedimentos para paginação
    paginator = Paginator(calendarios, 10)  # 10 calendários por página
    pagina = request.GET.get('page')
    calendarios = paginator.get_page(pagina)   

    context = {"calendarios": calendarios}
    
    return render(request, "calendario/lista_calendarios.html", context)

def editarCalendario(request, id):
    calendario = get_object_or_404(CalendarioAgricola, id=id)
    if request.method == "POST":
        form = CalendarioAgricolaForm(request.POST, instance=calendario)
        if form.is_valid():
            form.save()
            messages.success(request, "Calendário Agrícola atualizado com sucesso!")
            return redirect('calendarios')


# Views para Financiamentos
@login_required
def listaFinanciamentos(request):
    search = request.GET.get('search')
    
    if search:
        financiamentos = Financiamento.objects.filter(item__icontains=search).order_by('-data_inicio')
    else:
        financiamentos = Financiamento.objects.all().order_by('-data_inicio')
    
    paginator = Paginator(financiamentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'financiamento/lista_financiamentos.html', {'page_obj': page_obj, 'search': search})


@login_required
def editarFinanciamento(request, id):
    financiamento = get_object_or_404(Financiamento, id=id)
    
    if request.method == 'POST':
        form = FinanciamentoForm(request.POST, instance=financiamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Financiamento atualizado com sucesso!')
            return redirect('financiamentos')
    else:
        form = FinanciamentoForm(instance=financiamento)
    
    return render(request, 'financiamento/gerencia_financiamento.html', {'form': form, 'financiamento': financiamento})


@login_required
def cadastrarFinanciamento(request):
    if request.method == 'POST':
        form = FinanciamentoForm(request.POST)
        

        if form.is_valid():
            financiamento = form.save()
            # Criar as parcelas automaticamente
            financiamento.criar_parcelas()
            messages.success(request, 'Financiamento cadastrado com sucesso!')
            return redirect('financiamentos')
    else:
        form = FinanciamentoForm()
    
    return render(request, 'financiamento/gerencia_financiamento.html', {'form': form})


@login_required
def excluirFinanciamento(request, id):
    financiamento = get_object_or_404(Financiamento, id=id)
    financiamento.delete()
    messages.success(request, 'Financiamento excluído com sucesso!')
    return redirect('financiamentos')


@login_required
def detalhesFinanciamento(request, id):
    financiamento = get_object_or_404(Financiamento, id=id)
    parcelas = ParcelaFinanciamento.objects.filter(financiamento=financiamento).order_by('numero_parcela')
    
    return render(request, 'financiamento/detalhes_financiamento.html', {
        'financiamento': financiamento,
        'parcelas': parcelas
    })


@login_required
def pagarParcela(request, id):
    parcela = get_object_or_404(ParcelaFinanciamento, id=id)
    
    if request.method == 'POST':
        form = ParcelaFinanciamentoForm(request.POST, instance=parcela)
        form.is_valid()
        print(form.errors)
        if form.is_valid():
            parcela_salva = form.save()
            # Atualizar status do financiamento se necessário
            financiamento = parcela_salva.financiamento
            if financiamento.parcelas_pagas == financiamento.numero_parcelas:
                financiamento.status = 'QUITADO'
                financiamento.save()
            messages.success(request, 'Pagamento registrado com sucesso!')
            return redirect('detalhes_financiamento', id=financiamento.id)
    else:
        form = ParcelaFinanciamentoForm(instance=parcela)
    
    return render(request, 'financiamento/pagar_parcela.html', {
        'form': form,
        'parcela': parcela
    })

@login_required
def editarCalendario(request, id):
    calendario = get_object_or_404(CalendarioAgricola, id=id)
    if request.method == "POST":
        form = CalendarioAgricolaForm(request.POST, instance=calendario)
        if form.is_valid():
            form.save()
            messages.success(request, "Calendário Agrícola editado com sucesso!")
            return redirect('calendarios')
    else:
        form = CalendarioAgricolaForm(instance=calendario)

    return render(request, "calendario/gerencia_calendario.html", {"form": form, 'editar':True})

def cadastrarCalendario(request):
    if request.method == "POST":
        form = CalendarioAgricolaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Calendário Agrícola cadastrado com sucesso!")
            return redirect('calendarios')
    else:
        form = CalendarioAgricolaForm()

    return render(request, "calendario/gerencia_calendario.html", {"form": form})

def excluirCalendario(request, id):
    calendario = get_object_or_404(CalendarioAgricola, id=id)
    calendario.delete()
    messages.success(request, "Calendário Agrícola excluído com sucesso!")
    return redirect('calendarios')
