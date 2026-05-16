from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from .models import Perfil, Sistema, Usuario, UsuarioSistema
from .utils import (
    NOME_PERFIL_ADMINISTRADOR,
    NOME_PERFIL_PRODUTOR,
    NOME_SISTEMA_PRINCIPAL,
    garantir_perfis_base,
)


class CadastroUsuarioInternoTests(TestCase):
    def setUp(self):
        self.sistema, self.perfis = garantir_perfis_base()
        self.admin = self._criar_usuario_com_perfil(
            username='admin.local',
            email='admin.local@example.com',
            perfil_nome=NOME_PERFIL_ADMINISTRADOR,
        )
        self.produtor = self._criar_usuario_com_perfil(
            username='produtor.local',
            email='produtor.local@example.com',
            perfil_nome=NOME_PERFIL_PRODUTOR,
        )

    def _criar_usuario_com_perfil(self, username, email, perfil_nome):
        user = User.objects.create_user(
            username=username,
            email=email,
            password='SenhaForte@123',
            first_name='Teste',
            last_name='Usuario',
            is_staff=(perfil_nome == NOME_PERFIL_ADMINISTRADOR),
        )
        Usuario.objects.create(user=user, ativo=True)
        UsuarioSistema.objects.create(
            usuario=user,
            sistema=self.sistema,
            perfil=self.perfis[perfil_nome],
            ativo=True,
        )
        return user

    def test_administrador_pode_acessar_tela_de_cadastro(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse('usuarios:usuario_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/usuario_form.html')
        self.assertContains(response, 'Perfil de acesso')

    def test_produtor_nao_pode_acessar_tela_de_cadastro(self):
        self.client.force_login(self.produtor)

        response = self.client.get(reverse('usuarios:usuario_create'))

        self.assertRedirects(response, reverse('index'))
        mensagens = [mensagem.message for mensagem in get_messages(response.wsgi_request)]
        self.assertIn('Apenas usuários com perfil Administrador podem cadastrar usuários no sistema.', mensagens)

    def test_administrador_pode_criar_usuario_produtor(self):
        self.client.force_login(self.admin)

        response = self.client.post(reverse('usuarios:usuario_create'), {
            'username': 'joao.produtor',
            'first_name': 'Joao',
            'last_name': 'Produtor',
            'email': 'joao.produtor@example.com',
            'telefone': '(11) 99999-1111',
            'cargo': 'Produtor Rural',
            'departamento': 'Operacoes',
            'data_nascimento': '1990-01-10',
            'ativo': 'on',
            'perfil_acesso': self.perfis[NOME_PERFIL_PRODUTOR].pk,
            'password1': 'SenhaForte@123',
            'password2': 'SenhaForte@123',
        })

        self.assertRedirects(response, reverse('usuarios:usuario_list'))
        self.assertTrue(User.objects.filter(username='joao.produtor', email='joao.produtor@example.com').exists())

        usuario = Usuario.objects.select_related('user').get(user__username='joao.produtor')
        self.assertEqual(usuario.user.first_name, 'Joao')
        self.assertEqual(usuario.telefone, '(11) 99999-1111')
        self.assertTrue(usuario.ativo)
        self.assertFalse(usuario.user.is_staff)

        acesso = UsuarioSistema.objects.get(usuario=usuario.user, sistema__nome=NOME_SISTEMA_PRINCIPAL)
        self.assertEqual(acesso.perfil.nome, NOME_PERFIL_PRODUTOR)

    def test_administrador_pode_criar_outro_administrador(self):
        self.client.force_login(self.admin)

        response = self.client.post(reverse('usuarios:usuario_create'), {
            'username': 'admin.secundario',
            'first_name': 'Admin',
            'last_name': 'Secundario',
            'email': 'admin.secundario@example.com',
            'ativo': 'on',
            'perfil_acesso': self.perfis[NOME_PERFIL_ADMINISTRADOR].pk,
            'password1': 'SenhaForte@123',
            'password2': 'SenhaForte@123',
        })

        self.assertRedirects(response, reverse('usuarios:usuario_list'))

        user = User.objects.get(username='admin.secundario')
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

        acesso = UsuarioSistema.objects.get(usuario=user, sistema__nome=NOME_SISTEMA_PRINCIPAL)
        self.assertEqual(acesso.perfil.nome, NOME_PERFIL_ADMINISTRADOR)

    def test_administrador_pode_excluir_usuario(self):
        self.client.force_login(self.admin)

        response = self.client.post(reverse('usuarios:usuario_delete', args=[self.produtor.perfil_usuario.pk]))

        self.assertRedirects(response, reverse('usuarios:usuario_list'))
        self.assertFalse(User.objects.filter(pk=self.produtor.pk).exists())
        self.assertFalse(Usuario.objects.filter(user__username='produtor.local').exists())

    def test_nao_deve_permitir_excluir_o_proprio_usuario_logado(self):
        self.client.force_login(self.admin)

        response = self.client.post(reverse('usuarios:usuario_delete', args=[self.admin.perfil_usuario.pk]))

        self.assertRedirects(response, reverse('usuarios:usuario_list'))
        self.assertTrue(User.objects.filter(pk=self.admin.pk).exists())
        mensagens = [mensagem.message for mensagem in get_messages(response.wsgi_request)]
        self.assertIn('Não é permitido excluir o próprio usuário logado.', mensagens)
