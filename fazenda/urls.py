from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard-v3/', views.index, name='dashboardv3'),
    ################# Rotas para gerenciamento de Culturas #################
    path('culturas/', views.listaCulturas, name='culturas'),
    path('editar_cultura/<int:id>/', views.editarCultura, name='editar_cultura'),
    path('cadastrar_cultura/', views.cadastrarCultura, name='cadastrar_cultura'),
    path('excluir_cultura/<int:id>/', views.excluirCultura, name='excluir_cultura'),
    ################# Rotas para gerenciamento de Variedade de Culturas #################
    path('variedades/', views.listaVariedades, name='variedades'),
    path('editar_variedade/<int:id>/', views.editarVariedade, name='editar_variedade'),
    path('cadastrar_variedade/', views.cadastrarVariedade, name='cadastrar_variedade'),
    path('excluir_variedade/<int:id>/', views.excluirVariedade, name='excluir_variedade'),
    ################# Rotas para gerenciamento de Insumos #################
    path('insumos/', views.listaInsumos, name='insumos'),
    path('editar_insumo/<int:id>/', views.editarInsumo, name='editar_insumo'),
    path('cadastrar_insumo/', views.cadastrarInsumo, name='cadastrar_insumo'),
    path('excluir_insumo/<int:id>/', views.excluirInsumo, name='excluir_insumo'),
    ################# Rotas para gerenciamento de Tipo de Insumos #################
    path('tipo_insumos/', views.listaTipoInsumos, name='tipo_insumos'),
    path('editar_tipo_insumo/<int:id>/', views.editarTipoInsumo, name='editar_tipo_insumo'),
    path('cadastrar_tipo_insumo/', views.cadastrarTipoInsumo, name='cadastrar_tipo_insumo'),
    path('excluir_tipo_insumo/<int:id>/', views.excluirTipoInsumo, name='excluir_tipo_insumo'),
    ################# Rotas para gerenciamento de Tipo de Atividades #################
    path('tipo_atividades/', views.listaTipoAtividades, name='tipo_atividades'),
    path('editar_tipo_atividade/<int:id>/', views.editarTipoAtividade, name='editar_tipo_atividade'),
    path('cadastrar_tipo_atividade/', views.cadastrarTipoAtividade, name='cadastrar_tipo_atividade'),
    path('excluir_tipo_atividade/<int:id>/', views.excluirTipoAtividade, name='excluir_tipo_atividade'),
    ################# Rotas para gerenciamento de Quadras #################
    path('quadras/', views.listaQuadras, name='quadras'),
    path('editar_quadra/<int:id>/', views.editarQuadra, name='editar_quadra'),
    path('cadastrar_quadra/', views.cadastrarQuadra, name='cadastrar_quadra'),
    path('excluir_quadra/<int:id>/', views.excluirQuadra, name='excluir_quadra'),
    ################# Rotas para gerenciamento de Categorias de despesas #################
    path('categorias/', views.listaCategorias, name='categorias'),
    path('editar_categoria/<int:id>/', views.editarCategoria, name='editar_categoria'),
    path('cadastrar_categoria/', views.cadastrarCategoria, name='cadastrar_categoria'),
    path('excluir_categoria/<int:id>/', views.excluirCategoria, name='excluir_categoria'),
    ################# Rotas para gerenciamento de Tipo de Coleitas #################
    path('tipo_colheitas/', views.listaTipoColheitas, name='tipo_colheitas'),
    path('editar_tipo_colheita/<int:id>/', views.editarTipoColheita, name='editar_tipo_colheita'),
    path('cadastrar_tipo_colheita/', views.cadastrarTipoColheita, name='cadastrar_tipo_colheita'),
    path('excluir_tipo_colheita/<int:id>/', views.excluirTipoColheita, name='excluir_tipo_colheita'),
    ################# Rotas para gerenciamento de Despesas #################
    path('despesas/', views.listaDespesas, name='despesas'),
    path('editar_despesa/<int:id>/', views.editarDespesa, name='editar_despesa'),
    path('cadastrar_despesa/', views.cadastrarDespesa, name='cadastrar_despesa'),
    path('excluir_despesa/<int:id>/', views.excluirDespesa, name='excluir_despesa'),
    path('excluir_pagamento_despesa/<int:id>/', views.excluirPagamentoDespesa, name='excluir_pagamento_despesa'),
    ################# Rotas para gerenciamento de Colheitas #################
    path('colheitas/', views.listaColheitas, name='colheitas'),
    path('editar_colheita/<int:id>/', views.editarColheita, name='editar_colheita'),
    path('cadastrar_colheita/', views.cadastrarColheita, name='cadastrar_colheita'),
    path('excluir_colheita/<int:id>/', views.excluirColheita, name='excluir_colheita'),
    ################# Rotas para gerenciamento de Manejos #################
    path('manejos/', views.listaManejos, name='manejos'),
    path('editar_manejo/<int:id>/', views.editarManejo, name='editar_manejo'),
    path('cadastrar_manejo/', views.cadastrarManejo, name='cadastrar_manejo'),
    path('excluir_manejo/<int:id>/', views.excluirManejo, name='excluir_manejo'),
    
    # URLs################# Rotas para gerenciamento de Calendário Agrícola #################
    path('calendarios/', views.listaCalendarios, name='calendarios'),
    path('editar_calendario/<int:id>/', views.editarCalendario, name='editar_calendario'),
    path('cadastrar_calendario/', views.cadastrarCalendario, name='cadastrar_calendario'),
    path('excluir_calendario/<int:id>/', views.excluirCalendario, name='excluir_calendario'),
    ################# Rotas para gerenciamento de Financiamentos #################
    path('financiamentos/', views.listaFinanciamentos, name='financiamentos'),
    path('editar_financiamento/<int:id>/', views.editarFinanciamento, name='editar_financiamento'),
    path('cadastrar_financiamento/', views.cadastrarFinanciamento, name='cadastrar_financiamento'),
    path('excluir_financiamento/<int:id>/', views.excluirFinanciamento, name='excluir_financiamento'),
    path('detalhes_financiamento/<int:id>/', views.detalhesFinanciamento, name='detalhes_financiamento'),
    path('pagar_parcela/<int:id>/', views.pagarParcela, name='pagar_parcela'),
]
