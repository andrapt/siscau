from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Sistema, Funcao, Perfil, UsuarioSistema, Usuario
from .forms import (
    SistemaForm, FuncaoForm, PerfilForm, UsuarioSistemaForm, 
    UsuarioForm, UsuarioCadastroInternoForm, UsuarioEditForm, UsuarioFiltroForm
)
from .utils import administrador_required

# ============= VIEWS DE SISTEMA =============

@login_required
def sistema_list(request):
    """Lista todos os sistemas"""
    sistemas = Sistema.objects.all().order_by('nome')
    
    # Busca
    search = request.GET.get('search')
    if search:
        sistemas = sistemas.filter(
            Q(nome__icontains=search) | Q(descricao__icontains=search)
        )
    
    # Paginação
    paginator = Paginator(sistemas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'title': 'Sistemas'
    }
    return render(request, 'usuarios/sistema_list.html', context)

@login_required
def sistema_create(request):
    """Criar novo sistema"""
    if request.method == 'POST':
        form = SistemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sistema criado com sucesso!')
            return redirect('usuarios:sistema_list')
    else:
        form = SistemaForm()
    
    context = {
        'form': form,
        'title': 'Novo Sistema',
        'action': 'Criar'
    }
    return render(request, 'usuarios/sistema_form.html', context)

@login_required
def sistema_edit(request, pk):
    """Editar sistema"""
    sistema = get_object_or_404(Sistema, pk=pk)
    
    if request.method == 'POST':
        form = SistemaForm(request.POST, instance=sistema)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sistema atualizado com sucesso!')
            return redirect('usuarios:sistema_list')
    else:
        form = SistemaForm(instance=sistema)
    
    context = {
        'form': form,
        'sistema': sistema,
        'title': 'Editar Sistema',
        'action': 'Atualizar'
    }
    return render(request, 'usuarios/sistema_form.html', context)

@login_required
def sistema_delete(request, pk):
    """Deletar sistema"""
    sistema = get_object_or_404(Sistema, pk=pk)
    
    if request.method == 'POST':
        sistema.delete()
        messages.success(request, 'Sistema deletado com sucesso!')
        return redirect('usuarios:sistema_list')
    
    context = {
        'sistema': sistema,
        'title': 'Deletar Sistema'
    }
    return render(request, 'usuarios/sistema_confirm_delete.html', context)

# ============= VIEWS DE FUNÇÃO =============

@login_required
def funcao_list(request):
    """Lista todas as funções"""
    funcoes = Funcao.objects.all().order_by('nome')
    
    # Busca
    search = request.GET.get('search')
    if search:
        funcoes = funcoes.filter(
            Q(nome__icontains=search) | Q(codigo__icontains=search) | Q(descricao__icontains=search)
        )
    
    # Paginação
    paginator = Paginator(funcoes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    total_funcoes = Funcao.objects.count()
    funcoes_ativas = Funcao.objects.filter(ativo=True).count()
    funcoes_em_uso = Funcao.objects.filter(perfis__isnull=False).distinct().count()
    funcoes_sem_uso = total_funcoes - funcoes_em_uso
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'title': 'Funções',
        'total_funcoes': total_funcoes,
        'funcoes_ativas': funcoes_ativas,
        'funcoes_em_uso': funcoes_em_uso,
        'funcoes_sem_uso': funcoes_sem_uso,
    }
    return render(request, 'usuarios/funcao_list.html', context)

@login_required
def funcao_create(request):
    """Criar nova função"""
    if request.method == 'POST':
        form = FuncaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Função criada com sucesso!')
            return redirect('usuarios:funcao_list')
    else:
        form = FuncaoForm()
    
    context = {
        'form': form,
        'title': 'Nova Função',
        'action': 'Criar'
    }
    return render(request, 'usuarios/funcao_form.html', context)

@login_required
def funcao_edit(request, pk):
    """Editar função"""
    funcao = get_object_or_404(Funcao, pk=pk)
    
    if request.method == 'POST':
        form = FuncaoForm(request.POST, instance=funcao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Função atualizada com sucesso!')
            return redirect('usuarios:funcao_list')
    else:
        form = FuncaoForm(instance=funcao)
    
    context = {
        'form': form,
        'funcao': funcao,
        'title': 'Editar Função',
        'action': 'Atualizar'
    }
    return render(request, 'usuarios/funcao_form.html', context)

@login_required
def funcao_delete(request, pk):
    """Deletar função"""
    funcao = get_object_or_404(Funcao, pk=pk)
    
    if request.method == 'POST':
        funcao.delete()
        messages.success(request, 'Função deletada com sucesso!')
        return redirect('usuarios:funcao_list')
    
    context = {
        'funcao': funcao,
        'title': 'Deletar Função'
    }
    return render(request, 'usuarios/funcao_confirm_delete.html', context)

# ============= VIEWS DE PERFIL =============

@login_required
def perfil_list(request):
    """Lista todos os perfis"""
    perfis = Perfil.objects.select_related('sistema').prefetch_related('funcoes').order_by('sistema__nome', 'nome')
    
    # Filtros
    sistema_id = request.GET.get('sistema')
    if sistema_id:
        perfis = perfis.filter(sistema_id=sistema_id)
    
    search = request.GET.get('search')
    if search:
        perfis = perfis.filter(
            Q(nome__icontains=search) | Q(descricao__icontains=search) | Q(sistema__nome__icontains=search)
        )
    
    # Paginação
    paginator = Paginator(perfis, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Para o filtro de sistema
    sistemas = Sistema.objects.filter(ativo=True).order_by('nome')
    
    # Estatísticas
    total_perfis = Perfil.objects.count()
    perfis_ativos = Perfil.objects.filter(ativo=True).count()
    total_sistemas = Sistema.objects.count()
    usuarios_com_perfil = UsuarioSistema.objects.values('usuario').distinct().count()
    
    context = {
        'page_obj': page_obj,
        'sistemas': sistemas,
        'sistema_selecionado': sistema_id,
        'search': search,
        'title': 'Perfis',
        'total_perfis': total_perfis,
        'perfis_ativos': perfis_ativos,
        'total_sistemas': total_sistemas,
        'usuarios_com_perfil': usuarios_com_perfil,
    }
    return render(request, 'usuarios/perfil_list.html', context)

@login_required
def perfil_create(request):
    """Criar novo perfil"""
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil criado com sucesso!')
            return redirect('usuarios:perfil_list')
    else:
        form = PerfilForm()
    
    context = {
        'form': form,
        'title': 'Novo Perfil',
        'action': 'Criar'
    }
    return render(request, 'usuarios/perfil_form.html', context)

@login_required
def perfil_edit(request, pk):
    """Editar perfil"""
    perfil = get_object_or_404(Perfil, pk=pk)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:perfil_list')
    else:
        form = PerfilForm(instance=perfil)
    
    context = {
        'form': form,
        'perfil': perfil,
        'title': 'Editar Perfil',
        'action': 'Atualizar'
    }
    return render(request, 'usuarios/perfil_form.html', context)

@login_required
def perfil_delete(request, pk):
    """Deletar perfil"""
    perfil = get_object_or_404(Perfil, pk=pk)
    
    if request.method == 'POST':
        perfil.delete()
        messages.success(request, 'Perfil deletado com sucesso!')
        return redirect('usuarios:perfil_list')
    
    context = {
        'perfil': perfil,
        'title': 'Deletar Perfil'
    }
    return render(request, 'usuarios/perfil_confirm_delete.html', context)

# ============= VIEWS DE USUÁRIO =============

@administrador_required
def usuario_list(request):
    """Lista todos os usuários"""
    usuarios = Usuario.objects.select_related('user').order_by('user__username')
    
    # Filtros
    form = UsuarioFiltroForm(request.GET)
    if form.is_valid():
        nome = form.cleaned_data.get('nome')
        cargo = form.cleaned_data.get('cargo')
        departamento = form.cleaned_data.get('departamento')
        sistema = form.cleaned_data.get('sistema')
        ativo = form.cleaned_data.get('ativo')
        
        if nome:
            usuarios = usuarios.filter(
                Q(user__first_name__icontains=nome) | 
                Q(user__last_name__icontains=nome) | 
                Q(user__username__icontains=nome)
            )
        if cargo:
            usuarios = usuarios.filter(cargo__icontains=cargo)
        if departamento:
            usuarios = usuarios.filter(departamento__icontains=departamento)
        if sistema:
            usuarios = usuarios.filter(user__sistemas_acesso__sistema=sistema, user__sistemas_acesso__ativo=True).distinct()
        if ativo:
            usuarios = usuarios.filter(ativo=(ativo == 'True'))
    
    # Paginação
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'title': 'Usuários'
    }
    return render(request, 'usuarios/usuario_list.html', context)

@administrador_required
def usuario_create(request):
    """Criar novo usuário"""
    if request.method == 'POST':
        form = UsuarioCadastroInternoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('usuarios:usuario_list')
    else:
        form = UsuarioCadastroInternoForm()
    
    context = {
        'form': form,
        'title': 'Novo Usuário',
        'action': 'Criar'
    }
    return render(request, 'usuarios/usuario_form.html', context)

@administrador_required
def usuario_edit(request, pk):
    """Editar usuário"""
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('usuarios:usuario_list')
    else:
        form = UsuarioEditForm(instance=usuario)
    
    context = {
        'form': form,
        'usuario': usuario,
        'title': 'Editar Usuário',
        'action': 'Atualizar'
    }
    return render(request, 'usuarios/usuario_form.html', context)

@administrador_required
def usuario_detail(request, pk):
    """Detalhes do usuário"""
    usuario = get_object_or_404(Usuario, pk=pk)
    sistemas_acesso = UsuarioSistema.objects.filter(usuario=usuario.user).select_related('sistema', 'perfil')
    
    context = {
        'usuario': usuario,
        'sistemas_acesso': sistemas_acesso,
        'title': f'Usuário: {usuario.nome_completo}'
    }
    return render(request, 'usuarios/usuario_detail.html', context)

@administrador_required
def usuario_toggle_status(request, pk):
    """Ativar/Desativar usuário"""
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.method == 'POST':
        usuario.ativo = not usuario.ativo
        usuario.user.is_active = usuario.ativo
        usuario.user.save()
        usuario.save()
        
        status_text = "ativado" if usuario.ativo else "desativado"
        messages.success(request, f'Usuário {status_text} com sucesso!')
        return redirect('usuarios:usuario_list')
    
    context = {
        'usuario': usuario,
        'title': f'Confirmar {"Ativação" if not usuario.ativo else "Desativação"} do Usuário',
        'action': 'Ativar' if not usuario.ativo else 'Desativar'
    }
    return render(request, 'usuarios/usuario_confirm_toggle.html', context)

@administrador_required
def usuario_delete(request, pk):
    """Excluir usuário"""
    usuario = get_object_or_404(Usuario, pk=pk)
    total_acessos = UsuarioSistema.objects.filter(usuario=usuario.user).count()

    if request.method == 'POST':
        if request.user == usuario.user:
            messages.error(request, 'Não é permitido excluir o próprio usuário logado.')
            return redirect('usuarios:usuario_list')

        usuario.user.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('usuarios:usuario_list')

    context = {
        'usuario': usuario,
        'total_acessos': total_acessos,
        'title': f'Excluir Usuário: {usuario.nome_completo}',
    }
    return render(request, 'usuarios/usuario_confirm_delete.html', context)

# ============= VIEWS DE ACESSO DE USUÁRIO AO SISTEMA =============

@login_required
def usuario_sistema_list(request):
    """Lista todos os acessos de usuários aos sistemas"""
    acessos = UsuarioSistema.objects.select_related('usuario', 'sistema', 'perfil').order_by('usuario__username', 'sistema__nome')
    
    # Filtros
    sistema_id = request.GET.get('sistema')
    if sistema_id:
        acessos = acessos.filter(sistema_id=sistema_id)
    
    search = request.GET.get('search')
    if search:
        acessos = acessos.filter(
            Q(usuario__username__icontains=search) | 
            Q(usuario__first_name__icontains=search) | 
            Q(usuario__last_name__icontains=search) | 
            Q(sistema__nome__icontains=search) | 
            Q(perfil__nome__icontains=search)
        )
    
    # Paginação
    paginator = Paginator(acessos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Para o filtro de sistema
    sistemas = Sistema.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'page_obj': page_obj,
        'sistemas': sistemas,
        'sistema_selecionado': sistema_id,
        'search': search,
        'title': 'Acessos de Usuários'
    }
    return render(request, 'usuarios/usuario_sistema_list.html', context)

@login_required
def usuario_sistema_create(request):
    """Criar novo acesso de usuário ao sistema"""
    if request.method == 'POST':
        form = UsuarioSistemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Acesso criado com sucesso!')
            return redirect('usuarios:usuario_sistema_list')
    else:
        form = UsuarioSistemaForm()
    
    context = {
        'form': form,
        'title': 'Novo Acesso',
        'action': 'Criar'
    }
    return render(request, 'usuarios/usuario_sistema_form.html', context)

@login_required
def usuario_sistema_edit(request, pk):
    """Editar acesso de usuário ao sistema"""
    acesso = get_object_or_404(UsuarioSistema, pk=pk)
    
    if request.method == 'POST':
        form = UsuarioSistemaForm(request.POST, instance=acesso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Acesso atualizado com sucesso!')
            return redirect('usuarios:usuario_sistema_list')
    else:
        form = UsuarioSistemaForm(instance=acesso)
    
    context = {
        'form': form,
        'acesso': acesso,
        'title': 'Editar Acesso',
        'action': 'Atualizar'
    }
    return render(request, 'usuarios/usuario_sistema_form.html', context)

@login_required
def usuario_sistema_delete(request, pk):
    """Deletar acesso de usuário ao sistema"""
    acesso = get_object_or_404(UsuarioSistema, pk=pk)
    
    if request.method == 'POST':
        acesso.delete()
        messages.success(request, 'Acesso removido com sucesso!')
        return redirect('usuarios:usuario_sistema_list')
    
    context = {
        'acesso': acesso,
        'title': 'Remover Acesso'
    }
    return render(request, 'usuarios/usuario_sistema_confirm_delete.html', context)

# ============= VIEWS AJAX =============

def get_perfis_por_sistema(request):
    """Retorna perfis de um sistema específico via AJAX"""
    sistema_id = request.GET.get('sistema_id')
    perfis = Perfil.objects.filter(sistema_id=sistema_id, ativo=True).values('id', 'nome')
    return JsonResponse(list(perfis), safe=False)

# ============= VIEW PRINCIPAL =============

@login_required
def index(request):
    """Página principal do módulo de usuários"""
    # Estatísticas
    total_usuarios = Usuario.objects.filter(ativo=True).count()
    total_sistemas = Sistema.objects.filter(ativo=True).count()
    total_perfis = Perfil.objects.filter(ativo=True).count()
    total_funcoes = Funcao.objects.filter(ativo=True).count()
    total_acessos = UsuarioSistema.objects.filter(ativo=True).count()
    
    # Últimos usuários criados
    ultimos_usuarios = Usuario.objects.select_related('user').filter(ativo=True).order_by('-data_criacao')[:5]
    
    # Sistemas mais utilizados
    sistemas_populares = Sistema.objects.filter(
        ativo=True,
        usuarios_acesso__ativo=True
    ).distinct().order_by('-usuarios_acesso__data_acesso')[:5]
    
    context = {
        'total_usuarios': total_usuarios,
        'total_sistemas': total_sistemas,
        'total_perfis': total_perfis,
        'total_funcoes': total_funcoes,
        'total_acessos': total_acessos,
        'ultimos_usuarios': ultimos_usuarios,
        'sistemas_populares': sistemas_populares,
        'title': 'Controle de Usuários'
    }
    return render(request, 'usuarios/index.html', context)
