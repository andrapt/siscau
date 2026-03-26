from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Sistema, Funcao, Perfil, UsuarioSistema, Usuario

class SistemaForm(forms.ModelForm):
    class Meta:
        model = Sistema
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do sistema'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição do sistema'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nome': 'Nome do Sistema',
            'descricao': 'Descrição',
            'ativo': 'Sistema Ativo',
        }

class FuncaoForm(forms.ModelForm):
    class Meta:
        model = Funcao
        fields = ['nome', 'codigo', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da função'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único da função'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição da função'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nome': 'Nome da Função',
            'codigo': 'Código',
            'descricao': 'Descrição',
            'ativo': 'Função Ativa',
        }
    
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.upper().strip()
            # Verificar se já existe outro registro com o mesmo código
            if self.instance.pk:
                if Funcao.objects.exclude(pk=self.instance.pk).filter(codigo=codigo).exists():
                    raise ValidationError('Já existe uma função com este código.')
            else:
                if Funcao.objects.filter(codigo=codigo).exists():
                    raise ValidationError('Já existe uma função com este código.')
        return codigo

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome', 'sistema', 'funcoes', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do perfil'}),
            'sistema': forms.Select(attrs={'class': 'form-control'}),
            'funcoes': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição do perfil'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nome': 'Nome do Perfil',
            'sistema': 'Sistema',
            'funcoes': 'Funções',
            'descricao': 'Descrição',
            'ativo': 'Perfil Ativo',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas sistemas ativos
        self.fields['sistema'].queryset = Sistema.objects.filter(ativo=True)
        # Filtrar apenas funções ativas
        self.fields['funcoes'].queryset = Funcao.objects.filter(ativo=True)
    
    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        sistema = cleaned_data.get('sistema')
        
        if nome and sistema:
            # Verificar se já existe um perfil com o mesmo nome no mesmo sistema
            if self.instance.pk:
                if Perfil.objects.exclude(pk=self.instance.pk).filter(nome=nome, sistema=sistema).exists():
                    raise ValidationError('Já existe um perfil com este nome neste sistema.')
            else:
                if Perfil.objects.filter(nome=nome, sistema=sistema).exists():
                    raise ValidationError('Já existe um perfil com este nome neste sistema.')
        
        return cleaned_data

class UsuarioSistemaForm(forms.ModelForm):
    class Meta:
        model = UsuarioSistema
        fields = ['usuario', 'sistema', 'perfil', 'ativo']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'sistema': forms.Select(attrs={'class': 'form-control'}),
            'perfil': forms.Select(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'usuario': 'Usuário',
            'sistema': 'Sistema',
            'perfil': 'Perfil',
            'ativo': 'Acesso Ativo',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas sistemas ativos
        self.fields['sistema'].queryset = Sistema.objects.filter(ativo=True)
        # Filtrar apenas perfis ativos
        self.fields['perfil'].queryset = Perfil.objects.filter(ativo=True)
        
        # Se há um sistema selecionado, filtrar perfis por sistema
        if 'sistema' in self.data:
            try:
                sistema_id = int(self.data.get('sistema'))
                self.fields['perfil'].queryset = Perfil.objects.filter(sistema_id=sistema_id, ativo=True)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.sistema:
            self.fields['perfil'].queryset = Perfil.objects.filter(sistema=self.instance.sistema, ativo=True)
    
    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        sistema = cleaned_data.get('sistema')
        perfil = cleaned_data.get('perfil')
        
        # Verificar se o perfil pertence ao sistema
        if perfil and sistema and perfil.sistema != sistema:
            raise ValidationError('O perfil selecionado não pertence ao sistema escolhido.')
        
        # Verificar se o usuário já tem acesso ao sistema
        if usuario and sistema:
            if self.instance.pk:
                if UsuarioSistema.objects.exclude(pk=self.instance.pk).filter(usuario=usuario, sistema=sistema).exists():
                    raise ValidationError('Este usuário já possui acesso a este sistema.')
            else:
                if UsuarioSistema.objects.filter(usuario=usuario, sistema=sistema).exists():
                    raise ValidationError('Este usuário já possui acesso a este sistema.')
        
        return cleaned_data

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['telefone', 'cargo', 'departamento', 'data_nascimento', 'ativo']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo do usuário'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departamento'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'telefone': 'Telefone',
            'cargo': 'Cargo',
            'departamento': 'Departamento',
            'data_nascimento': 'Data de Nascimento',
            'ativo': 'Usuário Ativo',
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # Campos do perfil de usuário
    telefone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}))
    cargo = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    departamento = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_nascimento = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Criar o perfil de usuário
            Usuario.objects.create(
                user=user,
                telefone=self.cleaned_data.get('telefone', ''),
                cargo=self.cleaned_data.get('cargo', ''),
                departamento=self.cleaned_data.get('departamento', ''),
                data_nascimento=self.cleaned_data.get('data_nascimento'),
            )
        return user

class UsuarioEditForm(forms.ModelForm):
    """Formulário para editar dados do usuário Django + perfil"""
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Usuario
        fields = ['telefone', 'cargo', 'departamento', 'data_nascimento', 'ativo']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        
        if commit:
            # Atualizar dados do User
            usuario.user.first_name = self.cleaned_data['first_name']
            usuario.user.last_name = self.cleaned_data['last_name']
            usuario.user.email = self.cleaned_data['email']
            usuario.user.save()
            
            # Salvar o perfil
            usuario.save()
        
        return usuario

# Formulário para filtros de busca
class UsuarioFiltroForm(forms.Form):
    nome = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do usuário'}))
    cargo = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo'}))
    departamento = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departamento'}))
    sistema = forms.ModelChoiceField(queryset=Sistema.objects.filter(ativo=True), required=False, widget=forms.Select(attrs={'class': 'form-control'}), empty_label='Todos os sistemas')
    ativo = forms.ChoiceField(choices=[('', 'Todos'), ('True', 'Ativos'), ('False', 'Inativos')], required=False, widget=forms.Select(attrs={'class': 'form-control'}))