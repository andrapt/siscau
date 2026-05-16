from django.db import models
    
class Fazenda (models.Model):
    nome = models.CharField(max_length=45)
    localizacao = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'fazenda'

    def __str__(self):
        return self.nome

class Variedade (models.Model):    
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    class Meta:
        db_table = 'variedade'

    def __str__(self):
        return self.nome
    
class Cultura (models.Model):    
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    class Meta:
        db_table = 'cultura'

    def __str__(self):
        return self.nome
    
class Quadra(models.Model):   
    nome = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=6, decimal_places=2)
    tipoSolo = models.CharField(max_length=100, null=True, blank=True)
    dataPlantio = models.DateField(null=True, blank=True)
    espacamento = models.CharField(max_length=100, null=True, blank=True)
    variedades = models.ManyToManyField(Variedade, blank=True)
    culturas = models.ManyToManyField(Cultura, blank=True)
    descricao = models.TextField(null=True, blank=True)
    
    
    class Meta:
        db_table = 'quadra'

    def __str__(self):
        return self.nome

# Classe de Tipo de Insumo - 'fertilizante' ou 'defensivo'
class TipoInsumo (models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        db_table = 'tipo_insumo'

    def __str__(self):
          return self.nome
    
class Insumo (models.Model):    
    nome = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoInsumo, on_delete=models.CASCADE)
    fabricante = models.CharField(max_length=100, null=True, blank=True)
    formaFisica = models.CharField(max_length=100, null=True, blank=True)
    finalidade = models.CharField(max_length=100, null=True, blank=True)
    formulaComposicao = models.TextField(null=True, blank=True)
    aplicacao = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'insumo'

    def __str__(self):
            return self.nome

    
# Classe de Manejo (com custo)
class TipoAtividade (models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        db_table = 'tipo_atividade'

    def __str__(self):
          return self.nome

# Classe de Manejo (com custo)
class Manejo (models.Model):   
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE)
    tipoAtividade = models.ForeignKey(TipoAtividade, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null=True)
    dataInicio = models.DateField()
    dataFim = models.DateField(null=True, blank=True)
    responsavel = models.CharField(max_length=64)
    custoMaterial = models.DecimalField(max_digits=6, decimal_places=2)
    custoMaoObra = models.DecimalField(max_digits=6, decimal_places=2)
    dose = models.CharField(max_length=64, null=True, blank=True)
    unidade = models.CharField(max_length=10, null=True, blank=True) 
    descricao = models.TextField()
    
    class Meta:
        db_table = 'manejo'

    def __str__(self):
            return self.responsavel
    
# Classe de Tipo de Colheita - Integral / meia
class TipoColheita (models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        db_table = 'tipo_colheita'

    def __str__(self):
          return self.nome
    
# Classe de Colheita (com valor de venda) ex. frutos, amêndoas secas, etc.
class Colheita (models.Model): 
    VASSOURA_BRUXA_CHOICES = [
        ('', 'Nao se aplica'),
        ('COM', 'Cacau com vassoura de bruxa'),
        ('SEM', 'Cacau sem vassoura de bruxa'),
    ]

    data = models.DateField(null=True, blank=True)
    ano = models.IntegerField(default=2025)
    peso = models.DecimalField(max_digits=6, decimal_places=2)     
    preco = models.DecimalField(max_digits=6, decimal_places=2) # R$/kg
    valorTotal = models.DecimalField(max_digits=6, decimal_places=2)
    descricao = models.TextField(null=True, blank=True) 
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE)
    cultura = models.ForeignKey(Cultura, on_delete=models.SET_NULL, null=True, blank=True)
    variedade = models.ForeignKey(Variedade, on_delete=models.CASCADE)
    tipoColheita = models.ForeignKey(TipoColheita, on_delete=models.CASCADE)
    situacao_vassoura_bruxa = models.CharField(
        max_length=3,
        choices=VASSOURA_BRUXA_CHOICES,
        blank=True,
        default='',
    )

    class Meta:
        db_table = 'colheita'

    def __str__(self):
          return self.nome

# Classe de Categoria de Despesas - exemplo: energia, transporte, etc.
class Categoria (models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
          return self.nome

# Classe de Despesas Gerais
class Despesa (models.Model):   
    FONTE_DESPESA_CHOICES = [
        ('RECURSOS_FAZENDA', 'Recursos da fazenda'),
        ('FINANCIAMENTO', 'Financiamento'),
        ('ARLEY_PINTO', 'Arley Pinto'),
        ('ALBERTH_COUTO', 'Alberth Couto'),
        ('LAURA_MARIA', 'Laura Maria'),
    ]
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data = models.DateField(null=True, blank=True)
    descricao = models.CharField(max_length=256)  
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    fonte = models.CharField(max_length=20, choices=FONTE_DESPESA_CHOICES, default='RECURSOS_FAZENDA')
    
    class Meta:
        db_table = 'despesa'

    def __str__(self):
        return self.descricao

# Classe de calendário agrícola
class CalendarioAgricola (models.Model):
    MESES_CHOICES = [
        ('janeiro', 'Janeiro'),
        ('fevereiro', 'Fevereiro'),
        ('marco', 'Março'),
        ('abril', 'Abril'),
        ('maio', 'Maio'),
        ('junho', 'Junho'),
        ('julho', 'Julho'),
        ('agosto', 'Agosto'),
        ('setembro', 'Setembro'),
        ('outubro', 'Outubro'),
        ('novembro', 'Novembro'),
        ('dezembro', 'Dezembro'),
    ]
    
    cultura = models.ForeignKey(Cultura, on_delete=models.CASCADE) 
    mes = models.CharField(max_length=20, choices=MESES_CHOICES)
    descricao = models.TextField()
    atividades = models.TextField(help_text="Principais atividades do mês")
    observacoes = models.TextField(blank=True, null=True, help_text="Observações adicionais")
    
    class Meta:
        db_table = 'calendario_agricola'
        unique_together = ['cultura', 'mes']
        verbose_name = 'Calendário Agrícola'
        verbose_name_plural = 'Calendários Agrícolas'

    def __str__(self):
        return f"{self.cultura.nome} - {self.get_mes_display()}"

class Financiamento(models.Model):
    TIPO_CHOICES = [
        ('maquina', 'Máquina'),
        ('equipamento', 'Equipamento'),
        ('veiculo', 'Veículo'),
        ('implemento', 'Implemento'),
        ('infraestrutura', 'Infraestrutura'),
        ('outros', 'Outros'),
    ]
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('quitado', 'Quitado'),
        ('em_atraso', 'Em Atraso'),
        ('cancelado', 'Cancelado'),
    ]
    
    item = models.CharField(max_length=200, help_text="Descrição do item financiado")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='outros')
    valor_total = models.CharField(max_length=20, help_text="Valor total do item/equipamento")
    valor_entrada = models.CharField(max_length=20, help_text="Valor da entrada paga")
    valor_financiado = models.CharField(max_length=20, help_text="Valor efetivamente financiado")
    instituicao_financeira = models.CharField(max_length=100, help_text="Banco ou instituição financeira")
    taxa_juros = models.DecimalField(max_digits=5, decimal_places=2, help_text="Taxa de juros mensal (%)")
    numero_parcelas = models.IntegerField(help_text="Número total de parcelas")
    data_inicio = models.DateField(help_text="Data de início do financiamento")
    data_vencimento_primeira = models.DateField(help_text="Data de vencimento da primeira parcela")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'financiamento'
        verbose_name = 'Financiamento'
        verbose_name_plural = 'Financiamentos'
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f"{self.item} - {self.instituicao_financeira}"
    
    @property
    def valor_parcela(self):
        """Calcula o valor da parcela"""
        import re
        from decimal import Decimal
        if self.numero_parcelas > 0:
            # Converter valor_financiado de string para decimal
            valor_str = re.sub(r'[^\d,]', '', self.valor_financiado)
            valor_str = valor_str.replace(',', '.')
            valor_financiado_decimal = Decimal(valor_str) if valor_str else Decimal('0')
            return float(valor_financiado_decimal / self.numero_parcelas)
        return 0
    
    @property
    def parcelas_pagas(self):
        """Retorna o número de parcelas pagas"""
        return self.parcelafinanciamento_set.filter(status='pago').count()
    
    @property
    def parcelas_pendentes(self):
        """Retorna o número de parcelas pendentes"""
        return self.parcelafinanciamento_set.filter(status='pendente').count()
    
    @property
    def valor_pago(self):
        """Retorna o valor total já pago"""
        from decimal import Decimal
        return sum(parcela.valor_pago for parcela in self.parcelafinanciamento_set.filter(status='pago')) or Decimal('0')
    
    @property
    def valor_pendente(self):
        """Retorna o valor total pendente"""
        import re
        from decimal import Decimal
        # Converter valor_financiado de string para decimal
        valor_str = re.sub(r'[^\d,]', '', self.valor_financiado)
        valor_str = valor_str.replace(',', '.')
        valor_financiado_decimal = Decimal(valor_str) if valor_str else Decimal('0')
        return valor_financiado_decimal - self.valor_pago
    
    @property
    def percentual_pago(self):
        """Retorna o percentual pago do financiamento"""
        import re
        from decimal import Decimal
        # Converter valor_financiado de string para decimal
        valor_str = re.sub(r'[^\d,]', '', self.valor_financiado)
        valor_str = valor_str.replace(',', '.')
        valor_financiado_decimal = Decimal(valor_str) if valor_str else Decimal('0')
        if valor_financiado_decimal > 0:
            percentual = float((self.valor_pago / valor_financiado_decimal) * 100)
            # Garantir que o valor seja formatado com ponto decimal para CSS
            return f"{percentual:.4f}".replace(',', '.')
        return "0.0000"
    
    @property
    def percentual_pendente(self):
        """Retorna o percentual pendente do financiamento"""
        percentual_pago_float = float(self.percentual_pago)
        percentual_pendente = 100 - percentual_pago_float
        return f"{percentual_pendente:.4f}".replace(',', '.')
    
    def criar_parcelas(self):
        """Cria as parcelas do financiamento automaticamente"""
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        from decimal import Decimal
        import re
        
        # Converter valor_financiado de string para decimal
        valor_str = re.sub(r'[^\d,]', '', self.valor_financiado)
        valor_str = valor_str.replace(',', '.')
        valor_financiado_decimal = Decimal(valor_str) if valor_str else Decimal('0')
        
        # Calcular valor da parcela
        valor_parcela = valor_financiado_decimal / self.numero_parcelas if self.numero_parcelas > 0 else Decimal('0')
        
        # Criar as parcelas
        data_vencimento = self.data_vencimento_primeira
        
        for i in range(1, self.numero_parcelas + 1):
            ParcelaFinanciamento.objects.create(
                financiamento=self,
                numero_parcela=i,
                valor_parcela=valor_parcela,
                data_vencimento=data_vencimento,
                status='pendente'
            )
            # Próxima parcela vence no mês seguinte
            data_vencimento = data_vencimento + relativedelta(months=1)

class ParcelaFinanciamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('em_atraso', 'Em Atraso'),
        ('cancelado', 'Cancelado'),
    ]
    
    financiamento = models.ForeignKey(Financiamento, on_delete=models.CASCADE)
    numero_parcela = models.IntegerField(help_text="Número da parcela")
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor da parcela")
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Valor efetivamente pago")
    data_vencimento = models.DateField(help_text="Data de vencimento da parcela")
    data_pagamento = models.DateField(blank=True, null=True, help_text="Data do pagamento")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    juros_multa = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Juros e multa por atraso")
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'parcela_financiamento'
        verbose_name = 'Parcela de Financiamento'
        verbose_name_plural = 'Parcelas de Financiamento'
        ordering = ['financiamento', 'numero_parcela']
        unique_together = ['financiamento', 'numero_parcela']
    
    def __str__(self):
        return f"{self.financiamento.item} - Parcela {self.numero_parcela}/{self.financiamento.numero_parcelas}"
    
    @property
    def dias_atraso(self):
        """Calcula os dias de atraso se houver"""
        from datetime import date
        if self.status == 'pendente' and self.data_vencimento < date.today():
            return (date.today() - self.data_vencimento).days
        return 0
    
    @property
    def esta_em_atraso(self):
        """Verifica se a parcela está em atraso"""
        return self.dias_atraso > 0
    

    
