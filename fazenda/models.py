from calendar import monthrange
from datetime import date as date_cls
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Sum
    
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
    cultura = models.ForeignKey('Cultura', on_delete=models.SET_NULL, null=True, blank=True)
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
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('parcial', 'Parcial'),
        ('paga', 'Paga'),
    ]
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data = models.DateField(null=True, blank=True)
    data_primeiro_vencimento = models.DateField(null=True, blank=True)
    descricao = models.CharField(max_length=256)  
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    fonte = models.CharField(max_length=20, choices=FONTE_DESPESA_CHOICES, default='RECURSOS_FAZENDA')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aberta')
    quantidade_parcelas = models.PositiveIntegerField(default=1)
    
    class Meta:
        db_table = 'despesa'

    def __str__(self):
        return self.descricao

    @property
    def total_pago(self):
        total = self.pagamentos.aggregate(total=Sum('valor'))['total']
        return total or Decimal('0')

    @property
    def saldo_pendente(self):
        saldo = Decimal(self.valor or 0) - self.total_pago
        return saldo if saldo > 0 else Decimal('0')

    @property
    def quantidade_pagamentos(self):
        return self.pagamentos.count()

    @property
    def quantidade_parcelas_previstas(self):
        return self.parcelas.count()

    @property
    def possui_parcelas_previstas(self):
        return self.parcelas.exists()

    def atualizar_status(self, save=True):
        total_pago = self.total_pago
        valor_total = Decimal(self.valor or 0)

        if total_pago <= 0:
            self.status = 'aberta'
        elif total_pago < valor_total:
            self.status = 'parcial'
        else:
            self.status = 'paga'

        if save:
            self.save(update_fields=['status'])
        return self.status

    def _somar_meses(self, data_base, meses):
        novo_mes = data_base.month - 1 + meses
        ano = data_base.year + novo_mes // 12
        mes = novo_mes % 12 + 1
        dia = min(data_base.day, monthrange(ano, mes)[1])
        return date_cls(ano, mes, dia)

    def gerar_parcelas_previstas(self):
        if self.quantidade_parcelas < 1:
            raise ValidationError('A despesa deve ter pelo menos uma parcela.')

        data_base = self.data_primeiro_vencimento or self.data
        if not data_base:
            raise ValidationError('Informe a data do primeiro vencimento para gerar as parcelas.')

        parcelas_existentes = list(self.parcelas.all())
        parcelas_excedentes = [
            parcela for parcela in parcelas_existentes
            if parcela.numero_parcela > self.quantidade_parcelas
        ]
        if any(parcela.total_pago > 0 for parcela in parcelas_excedentes):
            raise ValidationError(
                'Nao e possivel reduzir a quantidade de parcelas porque existem pagamentos vinculados as parcelas excedentes.'
            )

        total_centavos = int((Decimal(self.valor) * 100).quantize(Decimal('1')))
        quantidade = self.quantidade_parcelas
        valor_base = total_centavos // quantidade
        restante = total_centavos % quantidade

        parcelas_criadas = 0
        parcelas_existentes_map = {
            parcela.numero_parcela: parcela
            for parcela in parcelas_existentes
        }

        with transaction.atomic():
            for numero in range(1, quantidade + 1):
                valor_centavos = valor_base + (1 if numero <= restante else 0)
                valor_previsto = Decimal(valor_centavos) / Decimal('100')
                data_vencimento = self._somar_meses(data_base, numero - 1)

                parcela = parcelas_existentes_map.get(numero)
                if parcela:
                    alterou = False
                    if parcela.valor_previsto != valor_previsto:
                        parcela.valor_previsto = valor_previsto
                        alterou = True
                    if parcela.data_vencimento != data_vencimento:
                        parcela.data_vencimento = data_vencimento
                        alterou = True
                    if alterou:
                        parcela.save(update_fields=['valor_previsto', 'data_vencimento'])
                    parcela.atualizar_status()
                    continue

                ParcelaDespesa.objects.create(
                    despesa=self,
                    numero_parcela=numero,
                    data_vencimento=data_vencimento,
                    valor_previsto=valor_previsto,
                )
                parcelas_criadas += 1

            if parcelas_excedentes:
                ParcelaDespesa.objects.filter(
                    despesa=self,
                    numero_parcela__gt=quantidade
                ).delete()

        return parcelas_criadas


class ParcelaDespesa(models.Model):
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('parcial', 'Parcial'),
        ('paga', 'Paga'),
    ]

    despesa = models.ForeignKey(Despesa, on_delete=models.CASCADE, related_name='parcelas')
    numero_parcela = models.PositiveIntegerField()
    data_vencimento = models.DateField()
    valor_previsto = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aberta')

    class Meta:
        db_table = 'parcela_despesa'
        ordering = ['numero_parcela']
        unique_together = ['despesa', 'numero_parcela']

    def __str__(self):
        return f'Parcela {self.numero_parcela} - {self.despesa.descricao}'

    @property
    def total_pago(self):
        total = self.pagamentos.aggregate(total=Sum('valor'))['total']
        return total or Decimal('0')

    @property
    def saldo_pendente(self):
        saldo = Decimal(self.valor_previsto or 0) - self.total_pago
        return saldo if saldo > 0 else Decimal('0')

    def atualizar_status(self, save=True):
        total_pago = self.total_pago
        valor_previsto = Decimal(self.valor_previsto or 0)

        if total_pago <= 0:
            self.status = 'aberta'
        elif total_pago < valor_previsto:
            self.status = 'parcial'
        else:
            self.status = 'paga'

        if save:
            self.save(update_fields=['status'])
        return self.status


class PagamentoDespesa(models.Model):
    despesa = models.ForeignKey(Despesa, on_delete=models.CASCADE, related_name='pagamentos')
    parcela = models.ForeignKey(ParcelaDespesa, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagamentos')
    data_pagamento = models.DateField()
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    numero_parcela = models.PositiveIntegerField(null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'pagamento_despesa'
        ordering = ['data_pagamento', 'numero_parcela', 'id']

    def __str__(self):
        return f'Pagamento {self.id} - {self.despesa.descricao}'

    def clean(self):
        super().clean()

        if self.valor is not None and self.valor <= 0:
            raise ValidationError({'valor': 'O valor do pagamento deve ser maior que zero.'})

        if not self.despesa_id or self.valor is None:
            return

        if self.parcela_id:
            if self.parcela.despesa_id != self.despesa_id:
                raise ValidationError({
                    'parcela': 'A parcela selecionada nao pertence a esta despesa.'
                })

            total_parcela_existente = (
                PagamentoDespesa.objects.filter(parcela_id=self.parcela_id)
                .exclude(pk=self.pk)
                .aggregate(total=Sum('valor'))['total']
                or Decimal('0')
            )
            if total_parcela_existente + self.valor > self.parcela.valor_previsto:
                raise ValidationError({
                    'valor': 'O total pago da parcela nao pode ultrapassar o valor previsto da parcela.'
                })

        total_existente = (
            PagamentoDespesa.objects.filter(despesa_id=self.despesa_id)
            .exclude(pk=self.pk)
            .aggregate(total=Sum('valor'))['total']
            or Decimal('0')
        )
        total_resultante = total_existente + self.valor

        if total_resultante > self.despesa.valor:
            raise ValidationError({
                'valor': 'O total de pagamentos nao pode ultrapassar o valor da despesa.'
            })

        if self.numero_parcela:
            if self.numero_parcela > self.despesa.quantidade_parcelas:
                raise ValidationError({
                    'numero_parcela': 'O numero da parcela nao pode ser maior que a quantidade de parcelas da despesa.'
                })

    def save(self, *args, **kwargs):
        if self.parcela_id and not self.numero_parcela:
            self.numero_parcela = self.parcela.numero_parcela
        self.full_clean()
        super().save(*args, **kwargs)
        self.despesa.atualizar_status()
        if self.parcela_id:
            self.parcela.atualizar_status()

    def delete(self, *args, **kwargs):
        despesa = self.despesa
        parcela = self.parcela
        super().delete(*args, **kwargs)
        despesa.atualizar_status()
        if parcela:
            parcela.atualizar_status()

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
    

    
