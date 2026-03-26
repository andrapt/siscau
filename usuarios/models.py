from django.db import models
from django.contrib.auth.models import User

class Sistema(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sistema'
        verbose_name = 'Sistema'
        verbose_name_plural = 'Sistemas'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Funcao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    codigo = models.CharField(max_length=50, unique=True, help_text="Código único da função")
    ativo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'funcao'
        verbose_name = 'Função'
        verbose_name_plural = 'Funções'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Perfil(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, related_name='perfis')
    funcoes = models.ManyToManyField(Funcao, related_name='perfis', blank=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'perfil'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['sistema__nome', 'nome']
        unique_together = ['nome', 'sistema']  # Nome único por sistema
    
    def __str__(self):
        return f"{self.sistema.nome} - {self.nome}"

class UsuarioSistema(models.Model):
    """Tabela intermediária para relacionamento Usuario-Sistema-Perfil"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sistemas_acesso')
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, related_name='usuarios_acesso')
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='usuarios_sistema')
    ativo = models.BooleanField(default=True)
    data_acesso = models.DateTimeField(auto_now_add=True)
    data_ultimo_acesso = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'usuario_sistema'
        verbose_name = 'Acesso de Usuário ao Sistema'
        verbose_name_plural = 'Acessos de Usuários aos Sistemas'
        unique_together = ['usuario', 'sistema']  # Um usuário só pode ter um perfil por sistema
        ordering = ['usuario__username', 'sistema__nome']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.sistema.nome} ({self.perfil.nome})"
    
    def clean(self):
        """Validação para garantir que o perfil pertence ao sistema"""
        from django.core.exceptions import ValidationError
        if self.perfil and self.sistema and self.perfil.sistema != self.sistema:
            raise ValidationError('O perfil deve pertencer ao sistema selecionado.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Usuario(models.Model):
    """Extensão do modelo User do Django"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_usuario')
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'usuario_perfil'
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
        ordering = ['user__username']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
    
    @property
    def nome_completo(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def sistemas_acesso(self):
        """Retorna os sistemas que o usuário tem acesso"""
        return Sistema.objects.filter(
            usuarios_acesso__usuario=self.user,
            usuarios_acesso__ativo=True
        ).distinct()
    
    def tem_acesso_sistema(self, sistema):
        """Verifica se o usuário tem acesso a um sistema específico"""
        return UsuarioSistema.objects.filter(
            usuario=self.user,
            sistema=sistema,
            ativo=True
        ).exists()
    
    def get_perfil_sistema(self, sistema):
        """Retorna o perfil do usuário em um sistema específico"""
        try:
            usuario_sistema = UsuarioSistema.objects.get(
                usuario=self.user,
                sistema=sistema,
                ativo=True
            )
            return usuario_sistema.perfil
        except UsuarioSistema.DoesNotExist:
            return None
    
    def get_funcoes_sistema(self, sistema):
        """Retorna as funções do usuário em um sistema específico"""
        perfil = self.get_perfil_sistema(sistema)
        if perfil:
            return perfil.funcoes.filter(ativo=True)
        return Funcao.objects.none()
    
    def tem_funcao(self, sistema, codigo_funcao):
        """Verifica se o usuário tem uma função específica em um sistema"""
        return self.get_funcoes_sistema(sistema).filter(codigo=codigo_funcao).exists()
