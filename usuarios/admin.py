from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Sistema, Funcao, Perfil, UsuarioSistema, Usuario

@admin.register(Sistema)
class SistemaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'data_criacao']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']
    list_per_page = 20

@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'codigo', 'descricao']
    ordering = ['nome']
    list_per_page = 20

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sistema', 'ativo', 'data_criacao']
    list_filter = ['sistema', 'ativo', 'data_criacao']
    search_fields = ['nome', 'descricao', 'sistema__nome']
    filter_horizontal = ['funcoes']
    ordering = ['sistema__nome', 'nome']
    list_per_page = 20
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "funcoes":
            kwargs["queryset"] = Funcao.objects.filter(ativo=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(UsuarioSistema)
class UsuarioSistemaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'sistema', 'perfil', 'ativo', 'data_acesso']
    list_filter = ['sistema', 'ativo', 'data_acesso']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'sistema__nome', 'perfil__nome']
    ordering = ['usuario__username', 'sistema__nome']
    list_per_page = 20
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "perfil":
            kwargs["queryset"] = Perfil.objects.filter(ativo=True)
        elif db_field.name == "sistema":
            kwargs["queryset"] = Sistema.objects.filter(ativo=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Inline para mostrar UsuarioSistema no admin do Usuario
class UsuarioSistemaInline(admin.TabularInline):
    model = UsuarioSistema
    extra = 1
    fields = ['sistema', 'perfil', 'ativo']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "perfil":
            kwargs["queryset"] = Perfil.objects.filter(ativo=True)
        elif db_field.name == "sistema":
            kwargs["queryset"] = Sistema.objects.filter(ativo=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'user', 'cargo', 'departamento', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'cargo', 'departamento', 'data_criacao']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'cargo', 'departamento']
    ordering = ['user__username']
    list_per_page = 20
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user', 'ativo')
        }),
        ('Informações Pessoais', {
            'fields': ('telefone', 'data_nascimento')
        }),
        ('Informações Profissionais', {
            'fields': ('cargo', 'departamento')
        }),
    )
    
    def nome_completo(self, obj):
        return obj.nome_completo
    nome_completo.short_description = 'Nome Completo'

# Estender o UserAdmin padrão do Django para incluir o perfil de usuário
class UserInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuário'
    fields = ['telefone', 'cargo', 'departamento', 'data_nascimento', 'ativo']

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserInline, UsuarioSistemaInline)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Desregistrar o UserAdmin padrão e registrar o customizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customizar títulos do admin
admin.site.site_header = "SISCAU - Administração"
admin.site.site_title = "SISCAU Admin"
admin.site.index_title = "Painel de Administração"
