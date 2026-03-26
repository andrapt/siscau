from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from usuarios.models import Sistema, Funcao, Perfil, Usuario, UsuarioSistema

class Command(BaseCommand):
    help = 'Insere dados de exemplo na aplicação usuarios'

    def handle(self, *args, **options):
        """Cria dados de exemplo para a aplicação usuarios"""
        
        self.stdout.write("Iniciando criação de dados de exemplo...")
        
        with transaction.atomic():
            # 1. Criar Sistemas
            self.stdout.write("\n1. Criando sistemas...")
            sistemas_data = [
                {
                    'nome': 'SISCAU',
                    'descricao': 'Sistema de Controle Agropecuário Unificado',
                    'ativo': True
                },
                {
                    'nome': 'Fazenda',
                    'descricao': 'Módulo de Gestão da Fazenda',
                    'ativo': True
                },
                {
                    'nome': 'Fertilizantes',
                    'descricao': 'Módulo de Controle de Fertilizantes',
                    'ativo': True
                },
                {
                    'nome': 'Financeiro',
                    'descricao': 'Sistema de Controle Financeiro',
                    'ativo': False  # Sistema em desenvolvimento
                }
            ]
            
            sistemas = {}
            for sistema_data in sistemas_data:
                sistema, created = Sistema.objects.get_or_create(
                    nome=sistema_data['nome'],
                    defaults=sistema_data
                )
                sistemas[sistema.nome] = sistema
                if created:
                    self.stdout.write(f"  ✓ Sistema '{sistema.nome}' criado")
                else:
                    self.stdout.write(f"  - Sistema '{sistema.nome}' já existe")
            
            # 2. Criar Funções
            self.stdout.write("\n2. Criando funções...")
            funcoes_data = [
                # Funções gerais
                {'codigo': 'VIEW_DASHBOARD', 'nome': 'Visualizar Dashboard', 'descricao': 'Acesso ao painel principal'},
                {'codigo': 'ADMIN_USERS', 'nome': 'Administrar Usuários', 'descricao': 'Gerenciar usuários do sistema'},
                {'codigo': 'ADMIN_SYSTEM', 'nome': 'Administração do Sistema', 'descricao': 'Configurações gerais do sistema'},
                
                # Funções da Fazenda
                {'codigo': 'FAZENDA_VIEW', 'nome': 'Visualizar Fazenda', 'descricao': 'Consultar dados da fazenda'},
                {'codigo': 'FAZENDA_EDIT', 'nome': 'Editar Fazenda', 'descricao': 'Modificar dados da fazenda'},
                {'codigo': 'CULTURA_MANAGE', 'nome': 'Gerenciar Culturas', 'descricao': 'Criar e editar culturas'},
                {'codigo': 'QUADRA_MANAGE', 'nome': 'Gerenciar Quadras', 'descricao': 'Administrar quadras da fazenda'},
                {'codigo': 'COLHEITA_MANAGE', 'nome': 'Gerenciar Colheitas', 'descricao': 'Registrar e controlar colheitas'},
                
                # Funções de Fertilizantes
                {'codigo': 'FERT_VIEW', 'nome': 'Visualizar Fertilizantes', 'descricao': 'Consultar dados de fertilizantes'},
                {'codigo': 'FERT_MANAGE', 'nome': 'Gerenciar Fertilizantes', 'descricao': 'Administrar fertilizantes'},
                {'codigo': 'APLICACAO_MANAGE', 'nome': 'Gerenciar Aplicações', 'descricao': 'Controlar aplicações de fertilizantes'},
                
                # Funções Financeiras
                {'codigo': 'FIN_VIEW', 'nome': 'Visualizar Financeiro', 'descricao': 'Consultar dados financeiros'},
                {'codigo': 'FIN_MANAGE', 'nome': 'Gerenciar Financeiro', 'descricao': 'Administrar dados financeiros'},
                {'codigo': 'RELATORIO_FIN', 'nome': 'Relatórios Financeiros', 'descricao': 'Gerar relatórios financeiros'},
            ]
            
            funcoes = {}
            for funcao_data in funcoes_data:
                funcao, created = Funcao.objects.get_or_create(
                    codigo=funcao_data['codigo'],
                    defaults=funcao_data
                )
                funcoes[funcao.codigo] = funcao
                if created:
                    self.stdout.write(f"  ✓ Função '{funcao.nome}' criada")
                else:
                    self.stdout.write(f"  - Função '{funcao.nome}' já existe")
            
            # 3. Criar Perfis
            self.stdout.write("\n3. Criando perfis...")
            perfis_data = [
                {
                    'nome': 'Administrador',
                    'descricao': 'Acesso total ao sistema',
                    'sistema': sistemas['SISCAU'],
                    'funcoes': ['VIEW_DASHBOARD', 'ADMIN_USERS', 'ADMIN_SYSTEM', 'FAZENDA_VIEW', 'FAZENDA_EDIT', 
                               'CULTURA_MANAGE', 'QUADRA_MANAGE', 'COLHEITA_MANAGE', 'FERT_VIEW', 'FERT_MANAGE', 
                               'APLICACAO_MANAGE', 'FIN_VIEW', 'FIN_MANAGE', 'RELATORIO_FIN']
                },
                {
                    'nome': 'Gerente da Fazenda',
                    'descricao': 'Gerenciamento completo da fazenda',
                    'sistema': sistemas['Fazenda'],
                    'funcoes': ['VIEW_DASHBOARD', 'FAZENDA_VIEW', 'FAZENDA_EDIT', 'CULTURA_MANAGE', 
                               'QUADRA_MANAGE', 'COLHEITA_MANAGE']
                },
                {
                    'nome': 'Operador da Fazenda',
                    'descricao': 'Operações básicas da fazenda',
                    'sistema': sistemas['Fazenda'],
                    'funcoes': ['VIEW_DASHBOARD', 'FAZENDA_VIEW', 'COLHEITA_MANAGE']
                },
                {
                    'nome': 'Técnico em Fertilizantes',
                    'descricao': 'Especialista em fertilizantes',
                    'sistema': sistemas['Fertilizantes'],
                    'funcoes': ['VIEW_DASHBOARD', 'FERT_VIEW', 'FERT_MANAGE', 'APLICACAO_MANAGE']
                },
                {
                    'nome': 'Consultor Fertilizantes',
                    'descricao': 'Consulta de dados de fertilizantes',
                    'sistema': sistemas['Fertilizantes'],
                    'funcoes': ['VIEW_DASHBOARD', 'FERT_VIEW']
                },
                {
                    'nome': 'Analista Financeiro',
                    'descricao': 'Análise e controle financeiro',
                    'sistema': sistemas['Financeiro'],
                    'funcoes': ['VIEW_DASHBOARD', 'FIN_VIEW', 'FIN_MANAGE', 'RELATORIO_FIN']
                }
            ]
            
            perfis = {}
            for perfil_data in perfis_data:
                perfil, created = Perfil.objects.get_or_create(
                    nome=perfil_data['nome'],
                    sistema=perfil_data['sistema'],
                    defaults={
                        'descricao': perfil_data['descricao'],
                        'ativo': True
                    }
                )
                
                # Adicionar funções ao perfil
                if created or not perfil.funcoes.exists():
                    funcoes_perfil = [funcoes[codigo] for codigo in perfil_data['funcoes'] if codigo in funcoes]
                    perfil.funcoes.set(funcoes_perfil)
                
                perfis[f"{perfil.nome}_{perfil.sistema.nome}"] = perfil
                if created:
                    self.stdout.write(f"  ✓ Perfil '{perfil.nome}' criado para sistema '{perfil.sistema.nome}'")
                else:
                    self.stdout.write(f"  - Perfil '{perfil.nome}' já existe para sistema '{perfil.sistema.nome}'")
            
            # 4. Criar Usuários
            self.stdout.write("\n4. Criando usuários...")
            usuarios_data = [
                {
                    'username': 'admin',
                    'email': 'admin@siscau.com',
                    'first_name': 'Administrador',
                    'last_name': 'Sistema',
                    'password': 'admin123',
                    'is_staff': True,
                    'is_superuser': True,
                    'perfil_data': {
                        'cargo': 'Administrador do Sistema',
                        'departamento': 'TI',
                        'telefone': '(11) 99999-9999'
                    }
                },
                {
                    'username': 'gerente.fazenda',
                    'email': 'gerente@fazenda.com',
                    'first_name': 'João',
                    'last_name': 'Silva',
                    'password': 'gerente123',
                    'perfil_data': {
                        'cargo': 'Gerente da Fazenda',
                        'departamento': 'Produção',
                        'telefone': '(11) 88888-8888'
                    }
                },
                {
                    'username': 'operador.campo',
                    'email': 'operador@fazenda.com',
                    'first_name': 'Maria',
                    'last_name': 'Santos',
                    'password': 'operador123',
                    'perfil_data': {
                        'cargo': 'Operadora de Campo',
                        'departamento': 'Produção',
                        'telefone': '(11) 77777-7777'
                    }
                },
                {
                    'username': 'tecnico.fert',
                    'email': 'tecnico@fertilizantes.com',
                    'first_name': 'Carlos',
                    'last_name': 'Oliveira',
                    'password': 'tecnico123',
                    'perfil_data': {
                        'cargo': 'Técnico em Fertilizantes',
                        'departamento': 'Técnico',
                        'telefone': '(11) 66666-6666'
                    }
                },
                {
                    'username': 'consultor.fert',
                    'email': 'consultor@fertilizantes.com',
                    'first_name': 'Ana',
                    'last_name': 'Costa',
                    'password': 'consultor123',
                    'perfil_data': {
                        'cargo': 'Consultora em Fertilizantes',
                        'departamento': 'Consultoria',
                        'telefone': '(11) 55555-5555'
                    }
                },
                {
                    'username': 'analista.fin',
                    'email': 'analista@financeiro.com',
                    'first_name': 'Pedro',
                    'last_name': 'Ferreira',
                    'password': 'analista123',
                    'perfil_data': {
                        'cargo': 'Analista Financeiro',
                        'departamento': 'Financeiro',
                        'telefone': '(11) 44444-4444'
                    }
                }
            ]
            
            usuarios = {}
            for usuario_data in usuarios_data:
                # Criar usuário Django
                user, created = User.objects.get_or_create(
                    username=usuario_data['username'],
                    defaults={
                        'email': usuario_data['email'],
                        'first_name': usuario_data['first_name'],
                        'last_name': usuario_data['last_name'],
                        'is_staff': usuario_data.get('is_staff', False),
                        'is_superuser': usuario_data.get('is_superuser', False),
                        'is_active': True
                    }
                )
                
                if created:
                    user.set_password(usuario_data['password'])
                    user.save()
                    self.stdout.write(f"  ✓ Usuário '{user.username}' criado")
                else:
                    self.stdout.write(f"  - Usuário '{user.username}' já existe")
                
                # Criar perfil do usuário
                perfil_usuario, perfil_created = Usuario.objects.get_or_create(
                    user=user,
                    defaults=usuario_data['perfil_data']
                )
                
                usuarios[user.username] = user
            
            # 5. Criar Acessos dos Usuários aos Sistemas
            self.stdout.write("\n5. Criando acessos dos usuários...")
            acessos_data = [
                # Admin - acesso a todos os sistemas
                {'usuario': 'admin', 'sistema': 'SISCAU', 'perfil': 'Administrador_SISCAU'},
                {'usuario': 'admin', 'sistema': 'Fazenda', 'perfil': 'Gerente da Fazenda_Fazenda'},
                {'usuario': 'admin', 'sistema': 'Fertilizantes', 'perfil': 'Técnico em Fertilizantes_Fertilizantes'},
                
                # Gerente da Fazenda
                {'usuario': 'gerente.fazenda', 'sistema': 'SISCAU', 'perfil': 'Administrador_SISCAU'},
                {'usuario': 'gerente.fazenda', 'sistema': 'Fazenda', 'perfil': 'Gerente da Fazenda_Fazenda'},
                
                # Operador de Campo
                {'usuario': 'operador.campo', 'sistema': 'Fazenda', 'perfil': 'Operador da Fazenda_Fazenda'},
                
                # Técnico em Fertilizantes
                {'usuario': 'tecnico.fert', 'sistema': 'Fertilizantes', 'perfil': 'Técnico em Fertilizantes_Fertilizantes'},
                {'usuario': 'tecnico.fert', 'sistema': 'Fazenda', 'perfil': 'Operador da Fazenda_Fazenda'},
                
                # Consultor em Fertilizantes
                {'usuario': 'consultor.fert', 'sistema': 'Fertilizantes', 'perfil': 'Consultor Fertilizantes_Fertilizantes'},
                
                # Analista Financeiro
                {'usuario': 'analista.fin', 'sistema': 'Financeiro', 'perfil': 'Analista Financeiro_Financeiro'},
            ]
            
            for acesso_data in acessos_data:
                usuario = usuarios[acesso_data['usuario']]
                sistema = sistemas[acesso_data['sistema']]
                perfil = perfis[acesso_data['perfil']]
                
                acesso, created = UsuarioSistema.objects.get_or_create(
                    usuario=usuario,
                    sistema=sistema,
                    perfil=perfil,
                    defaults={'ativo': True}
                )
                
                if created:
                    self.stdout.write(f"  ✓ Acesso criado: {usuario.username} -> {sistema.nome} ({perfil.nome})")
                else:
                    self.stdout.write(f"  - Acesso já existe: {usuario.username} -> {sistema.nome} ({perfil.nome})")
        
        self.stdout.write("\n✅ Dados de exemplo criados com sucesso!")
        self.stdout.write("\n📊 Resumo:")
        self.stdout.write(f"  • Sistemas: {Sistema.objects.count()}")
        self.stdout.write(f"  • Funções: {Funcao.objects.count()}")
        self.stdout.write(f"  • Perfis: {Perfil.objects.count()}")
        self.stdout.write(f"  • Usuários: {User.objects.count()}")
        self.stdout.write(f"  • Acessos: {UsuarioSistema.objects.count()}")
        
        self.stdout.write("\n🔑 Credenciais de acesso:")
        self.stdout.write("  • admin / admin123 (Administrador)")
        self.stdout.write("  • gerente.fazenda / gerente123 (Gerente)")
        self.stdout.write("  • operador.campo / operador123 (Operador)")
        self.stdout.write("  • tecnico.fert / tecnico123 (Técnico)")
        self.stdout.write("  • consultor.fert / consultor123 (Consultor)")
        self.stdout.write("  • analista.fin / analista123 (Analista)")