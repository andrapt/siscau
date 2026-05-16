from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    
    # URLs de Sistema
    path('sistemas/', views.sistema_list, name='sistema_list'),
    path('sistemas/novo/', views.sistema_create, name='sistema_create'),
    path('sistemas/<int:pk>/editar/', views.sistema_edit, name='sistema_edit'),
    path('sistemas/<int:pk>/deletar/', views.sistema_delete, name='sistema_delete'),
    
    # URLs de Função
    path('funcoes/', views.funcao_list, name='funcao_list'),
    path('funcoes/nova/', views.funcao_create, name='funcao_create'),
    path('funcoes/<int:pk>/editar/', views.funcao_edit, name='funcao_edit'),
    path('funcoes/<int:pk>/deletar/', views.funcao_delete, name='funcao_delete'),
    
    # URLs de Perfil
    path('perfis/', views.perfil_list, name='perfil_list'),
    path('perfis/novo/', views.perfil_create, name='perfil_create'),
    path('perfis/<int:pk>/editar/', views.perfil_edit, name='perfil_edit'),
    path('perfis/<int:pk>/deletar/', views.perfil_delete, name='perfil_delete'),
    
    # URLs de Usuário
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/novo/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.usuario_edit, name='usuario_edit'),
    path('usuarios/<int:pk>/toggle-status/', views.usuario_toggle_status, name='usuario_toggle_status'),
    path('usuarios/<int:pk>/deletar/', views.usuario_delete, name='usuario_delete'),
    path('usuarios/<int:pk>/', views.usuario_detail, name='usuario_detail'),
    
    # URLs de Acesso de Usuário ao Sistema
    path('acessos/', views.usuario_sistema_list, name='usuario_sistema_list'),
    path('acessos/novo/', views.usuario_sistema_create, name='usuario_sistema_create'),
    path('acessos/<int:pk>/editar/', views.usuario_sistema_edit, name='usuario_sistema_edit'),
    path('acessos/<int:pk>/deletar/', views.usuario_sistema_delete, name='usuario_sistema_delete'),
    
    # URLs AJAX
    path('ajax/perfis-por-sistema/', views.get_perfis_por_sistema, name='get_perfis_por_sistema'),
]
