from django import forms
from .models import Cultura, Variedade, TipoInsumo, Insumo, TipoAtividade, Colheita, Quadra, Categoria, TipoColheita, Despesa, Manejo, CalendarioAgricola, Financiamento, ParcelaFinanciamento

class CulturaForm(forms.ModelForm):
    class Meta:
        model = Cultura
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),               
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),            
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 4 caracteres.")
        return nome
    
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           for field_name, field in self.fields.items():
               if field.required:
                   self.fields[field_name].label = f'{field.label} *'


class ManejoForm(forms.ModelForm):
    class Meta:
        model = Manejo 
        fields = "__all__"
        labels = { 
            'quadra': 'Quadra',
            'tipoAtividade': 'Tipo de Atividade',
            'insumo': 'Insumo',
            'dataInicio': 'Data de Início',
            'dataFim': 'Data de Término',
            'responsavel': 'Responsável',
            'custoMaterial': 'Custo do Material (R$)',
            'custoMaoObra': 'Custo da Mão de Obra (R$)',
            'dose': 'Dose',
            'unidade': 'Unidade',
            'descricao': 'Descrição'
        }
        widgets = {
            'quadra': forms.Select(attrs={'class': 'form-control'}),
            'tipoAtividade': forms.Select(attrs={'class': 'form-control'}),
            'insumo': forms.Select(attrs={'class': 'form-control'}),
            'dataInicio': forms.DateInput(attrs={'type': 'date','style': 'width: 100%;height: 40px; margin: 0 auto; display: block;','class': 'form-control'}, format='%Y-%m-%d'),
            'dataFim': forms.DateInput(attrs={'type': 'date','style': 'width: 100%;height: 40px; margin: 0 auto; display: block;','class': 'form-control'}, format='%Y-%m-%d'),
            'responsavel': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite o nome do responsável'}),
            'custoMaterial': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Digite o custo do material', 'id': 'id_custoMaterial'}),
            'custoMaoObra': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Digite o custo da mão de obra', 'id': 'id_custoMaoObra'}),
            'dose': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite a dose aplicada'}),
            'unidade': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite a unidade de medida'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           for field_name, field in self.fields.items():
               if field.required:
                   self.fields[field_name].label = f'{field.label} *'
    
class VariedadeForm(forms.ModelForm):
    class Meta:
        model = Variedade
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da variedade',}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 4 caracteres.")
        return nome

class TipoInsumoForm(forms.ModelForm):
    class Meta:
        model = TipoInsumo
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do tipo de insumo',})
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 4 caracteres.")
        return nome
    
class InsumoForm (forms.ModelForm):  
    class Meta:
        model = Insumo
        fields = '__all__'
        labels = { #Renomeação dos labels para titulos de maior facilidade de compreenção.
            'nome': 'Nome do insumo',
            'formaFisica': 'Forma Física',
            'formulaComposicao': 'Composição da fórmula',
            'aplicacao': 'Modo de aplicação'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control'}),
            'formaFisica': forms.TextInput(attrs={'class': 'form-control'}),
            'finalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'formulaComposicao': forms.Textarea(attrs={'class': 'form-control'}),
            'aplicacao': forms.Textarea(attrs={'class': 'form-control'})
        }  
        def clean_nome(self):
            nome = self.cleaned_data['nome'].strip()
            if len(nome) < 3:
                raise forms.ValidationError("O nome deve ter pelo menos 4 caracteres.")
            return nome
        
class TipoAtividadeForm(forms.ModelForm):
    class Meta:
        model = TipoAtividade
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do tipo de atividade',})
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 4 caracteres.")
        return nome

class QuadraForm(forms.ModelForm):
    class Meta:
        model = Quadra 
        fields = "__all__"
        labels = { 
            'nome': 'Nome da quadra',
            'area': 'Área da Quadra (ha)',
            'tipoSolo': 'Tipo de Solo',
            'dataPlantio': 'Data do plantio',
            'espacamento': 'Espaçamento entre plantas',
            'culturas': 'Culturas existentes na quadra',
            'variedades': 'Variedades existentes na quadra',
            'descricao': 'Descrição da quadra'
            
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite o nome da quadra'}),
            'area': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite a área da quadra'}),
            'tipoSolo': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite o nome da quadra',}),
            'dataPlantio': forms.DateInput(attrs={'type': 'date','style': 'width: 100%;height: 40px; margin: 0 auto; display: block;','class': 'form-control'}, format='%Y-%m-%d'),
            'espacamento': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite o espaçamento entre plantas',}),
            'variedades': forms.SelectMultiple(attrs={'class': 'form-control','placeholder': 'Selecione as variedades',}),
            'culturas': forms.SelectMultiple(attrs={'class': 'form-control','placeholder': 'Selecione as culturas',}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 4 caracteres.")
        return nome
    
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           for field_name, field in self.fields.items():
               if field.required:
                   self.fields[field_name].label = f'{field.label} *'


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da categoria',})
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 4 caracteres.")
        return nome
    
class TipoColheitaForm(forms.ModelForm):
    class Meta:
        model = TipoColheita
        fields = '__all__'
        labels = { 
            'nome': 'Nome'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do Tipo de Colheita',})
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 4 caracteres.")
        return nome
    

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa 
        fields = "__all__"
        labels = { 
            'categoria': 'Categoria',
            'data': 'Data',
            'valor': 'Valor',
            'descricao': 'Descrição da despesa',
            'fonte': 'Fonte de Despesa'
        }
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date','style': 'width: 100%;height: 40px; margin: 0 auto; display: block;','class': 'form-control'}, format='%Y-%m-%d'),
            'valor': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite a área da quadra'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'fonte': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_nome(self):
        nome = self.cleaned_data['descricao'].strip()
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 4 caracteres.")
        return nome
    
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           for field_name, field in self.fields.items():
               if field.required:
                   self.fields[field_name].label = f'{field.label} *'


class ColheitaForm(forms.ModelForm):
    class Meta:
        model = Colheita 
        fields = "__all__"
        labels = { 
            'data': 'Data da Colheita',
            'ano': 'Ano da Safra',
            'peso': 'Peso (kg)',
            'preco': 'Preço por kg (R$)',
            'valorTotal': 'Valor Total (R$)',
            'descricao': 'Descrição',
            'quadra': 'Quadra',
            'variedade': 'Variedade',
            'tipoColheita': 'Tipo de Colheita'
        }
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date','style': 'width: 100%;height: 40px; margin: 0 auto; display: block;','class': 'form-control'}, format='%Y-%m-%d'),
            'ano': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Digite o ano da safra'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Digite o peso em kg', 'id': 'peso', 'onchange': 'calcularValorTotal()'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Digite o preço por kg', 'id': 'preco', 'onchange': 'calcularValorTotal()'}),
            'valorTotal': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Valor total', 'id': 'valorTotal', 'readonly': 'readonly'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'quadra': forms.Select(attrs={'class': 'form-control'}),
            'variedade': forms.Select(attrs={'class': 'form-control'}),
            'tipoColheita': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           for field_name, field in self.fields.items():
               if field.required:
                   self.fields[field_name].label = f'{field.label} *'

class CalendarioAgricolaForm(forms.ModelForm):
    class Meta:
        model = CalendarioAgricola
        fields = '__all__'
        labels = { 
            'cultura': 'Cultura',
            'mes': 'Mês',
            'descricao': 'Descrição',
            'atividades': 'Principais Atividades',
            'observacoes': 'Observações'
        }
        widgets = {
            'cultura': forms.Select(attrs={'class': 'form-control'}),
            'mes': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'atividades': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome:
            return nome.title()
        return nome
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                self.fields[field_name].label = f'{field.label} *'


class FinanciamentoForm(forms.ModelForm):
    class Meta:
        model = Financiamento
        fields = '__all__'
        labels = {
            'item': 'Item/Equipamento',
            'tipo': 'Tipo de Financiamento',
            'valor_total': 'Valor Total (R$)',
            'valor_entrada': 'Entrada (R$)',
            'valor_financiado': 'Valor Financiado (R$)',
            'instituicao_financeira': 'Instituição Financeira',
            'taxa_juros': 'Taxa de Juros (% a.m.)',
            'numero_parcelas': 'Número de Parcelas',
            'data_inicio': 'Data de Início',
            'data_vencimento_primeira': 'Vencimento da 1ª Parcela',
            'status': 'Status',
            'observacoes': 'Observações'
        }
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do item/equipamento'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'valor_total': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o valor total', 'id': 'id_valor_total', 'onchange': 'calcularValorFinanciado()'}),
            'valor_entrada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o valor da entrada', 'id': 'id_valor_entrada', 'onchange': 'calcularValorFinanciado()'}),
            'valor_financiado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valor financiado', 'id': 'id_valor_financiado'}),
            'instituicao_financeira': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da instituição'}),
            'taxa_juros': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a taxa de juros', 'step': '0.01'}),
            'numero_parcelas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o número de parcelas'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'data_vencimento_primeira': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def clean_valor_entrada(self):
        valor_entrada = self.cleaned_data.get('valor_entrada', 0)
        valor_total = self.cleaned_data.get('valor_total', 0)
        if valor_entrada > valor_total:
            raise forms.ValidationError("O valor da entrada não pode ser maior que o valor total.")
        return valor_entrada

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                self.fields[field_name].label = f'{field.label} *'


class ParcelaFinanciamentoForm(forms.ModelForm):
    class Meta:
        model = ParcelaFinanciamento
        fields = ['valor_pago', 'data_pagamento', 'status', 'juros_multa', 'observacoes']
        labels = {
            'valor_pago': 'Valor Pago (R$)',
            'data_pagamento': 'Data do Pagamento',
            'status': 'Status',
            'juros_multa': 'Juros/Multa (R$)',
            'observacoes': 'Observações'
        }
        widgets = {
            'valor_pago': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o valor pago', 'step': '0.01', 'required': True}),
            'data_pagamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}, format='%Y-%m-%d'),
            'status': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'juros_multa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite juros/multa', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir campos obrigatórios
        self.fields['valor_pago'].required = True
        self.fields['data_pagamento'].required = True
        self.fields['status'].required = True
        
        # Adicionar asterisco aos campos obrigatórios
        for field_name, field in self.fields.items():
            if field.required:
                self.fields[field_name].label = f'{field.label} *'
                # Adicionar classe CSS para destacar campos obrigatórios
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' required-field'
                else:
                    field.widget.attrs['class'] = 'form-control required-field'
    
    def clean_valor_pago(self):
        valor_pago = self.cleaned_data.get('valor_pago')
        if valor_pago is None or valor_pago <= 0:
            raise forms.ValidationError('O valor pago deve ser maior que zero.')
        return valor_pago
    
    def clean_data_pagamento(self):
        data_pagamento = self.cleaned_data.get('data_pagamento')
        if not data_pagamento:
            raise forms.ValidationError('A data do pagamento é obrigatória.')
        return data_pagamento
    
    def clean_status(self):
        status = self.cleaned_data.get('status')
        if not status:
            raise forms.ValidationError('O status é obrigatório.')
        return status
 