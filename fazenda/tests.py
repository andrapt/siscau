from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Despesa, PagamentoDespesa


class DespesaPagamentoTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome='Energia')
        self.despesa = Despesa.objects.create(
            categoria=self.categoria,
            data=date(2026, 5, 18),
            data_primeiro_vencimento=date(2026, 6, 18),
            descricao='Compra de insumos',
            valor=Decimal('1000.00'),
            quantidade_parcelas=5,
            fonte='RECURSOS_FAZENDA',
        )

    def test_despesa_nova_inicia_aberta(self):
        self.assertEqual(self.despesa.status, 'aberta')
        self.assertEqual(self.despesa.total_pago, Decimal('0'))
        self.assertEqual(self.despesa.saldo_pendente, Decimal('1000.00'))

    def test_pagamento_parcial_altera_status_para_parcial(self):
        PagamentoDespesa.objects.create(
            despesa=self.despesa,
            data_pagamento=date(2026, 5, 20),
            valor=Decimal('250.00'),
            numero_parcela=1,
        )

        self.despesa.refresh_from_db()
        self.assertEqual(self.despesa.status, 'parcial')
        self.assertEqual(self.despesa.total_pago, Decimal('250.00'))
        self.assertEqual(self.despesa.saldo_pendente, Decimal('750.00'))

    def test_pagamento_total_altera_status_para_paga(self):
        PagamentoDespesa.objects.create(
            despesa=self.despesa,
            data_pagamento=date(2026, 5, 20),
            valor=Decimal('500.00'),
            numero_parcela=1,
        )
        PagamentoDespesa.objects.create(
            despesa=self.despesa,
            data_pagamento=date(2026, 6, 20),
            valor=Decimal('500.00'),
            numero_parcela=2,
        )

        self.despesa.refresh_from_db()
        self.assertEqual(self.despesa.status, 'paga')
        self.assertEqual(self.despesa.saldo_pendente, Decimal('0'))

    def test_nao_permite_ultrapassar_valor_total_da_despesa(self):
        PagamentoDespesa.objects.create(
            despesa=self.despesa,
            data_pagamento=date(2026, 5, 20),
            valor=Decimal('900.00'),
            numero_parcela=1,
        )

        with self.assertRaises(ValidationError):
            pagamento = PagamentoDespesa(
                despesa=self.despesa,
                data_pagamento=date(2026, 6, 20),
                valor=Decimal('200.00'),
                numero_parcela=2,
            )
            pagamento.full_clean()

    def test_gera_parcelas_previstas_distribuindo_valor_total(self):
        quantidade = self.despesa.gerar_parcelas_previstas()

        self.assertEqual(quantidade, 5)
        self.assertEqual(self.despesa.parcelas.count(), 5)
        self.assertEqual(
            sum(parcela.valor_previsto for parcela in self.despesa.parcelas.all()),
            Decimal('1000.00')
        )
        primeira = self.despesa.parcelas.first()
        self.assertEqual(primeira.numero_parcela, 1)
        self.assertEqual(primeira.data_vencimento, date(2026, 6, 18))

    def test_parcela_aceita_pagamentos_parciais_sem_ultrapassar_previsto(self):
        self.despesa.gerar_parcelas_previstas()
        parcela = self.despesa.parcelas.first()

        PagamentoDespesa.objects.create(
            despesa=self.despesa,
            parcela=parcela,
            data_pagamento=date(2026, 6, 18),
            valor=Decimal('100.00'),
        )
        PagamentoDespesa.objects.create(
            despesa=self.despesa,
            parcela=parcela,
            data_pagamento=date(2026, 6, 19),
            valor=Decimal('100.00'),
        )

        parcela.refresh_from_db()
        self.assertEqual(parcela.status, 'paga')
        self.assertEqual(parcela.total_pago, Decimal('200.00'))

    def test_gera_parcelas_remove_excedentes_sem_pagamento(self):
        self.despesa.gerar_parcelas_previstas()
        self.despesa.quantidade_parcelas = 3
        self.despesa.save(update_fields=['quantidade_parcelas'])

        self.despesa.gerar_parcelas_previstas()

        self.assertEqual(self.despesa.parcelas.count(), 3)
        self.assertFalse(self.despesa.parcelas.filter(numero_parcela__gt=3).exists())

    def test_nao_reduz_parcelas_quando_excedentes_tem_pagamento(self):
        self.despesa.gerar_parcelas_previstas()
        parcela = self.despesa.parcelas.get(numero_parcela=5)
        PagamentoDespesa.objects.create(
            despesa=self.despesa,
            parcela=parcela,
            data_pagamento=date(2026, 10, 18),
            valor=Decimal('50.00'),
        )
        self.despesa.quantidade_parcelas = 3
        self.despesa.save(update_fields=['quantidade_parcelas'])

        with self.assertRaises(ValidationError):
            self.despesa.gerar_parcelas_previstas()


class DespesaViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='123456')
        self.client.force_login(self.user)
        self.categoria = Categoria.objects.create(nome='Energia')
        self.aberta = Despesa.objects.create(
            categoria=self.categoria,
            data=date(2026, 5, 18),
            descricao='Conta aberta',
            valor=Decimal('100.00'),
            quantidade_parcelas=1,
            fonte='RECURSOS_FAZENDA',
        )
        self.parcial = Despesa.objects.create(
            categoria=self.categoria,
            data=date(2026, 5, 19),
            descricao='Conta parcial',
            valor=Decimal('200.00'),
            quantidade_parcelas=2,
            fonte='RECURSOS_FAZENDA',
        )
        PagamentoDespesa.objects.create(
            despesa=self.parcial,
            data_pagamento=date(2026, 5, 20),
            valor=Decimal('50.00'),
            numero_parcela=1,
        )
        self.paga = Despesa.objects.create(
            categoria=self.categoria,
            data=date(2026, 5, 20),
            descricao='Conta paga',
            valor=Decimal('300.00'),
            quantidade_parcelas=1,
            fonte='RECURSOS_FAZENDA',
        )
        PagamentoDespesa.objects.create(
            despesa=self.paga,
            data_pagamento=date(2026, 5, 21),
            valor=Decimal('300.00'),
            numero_parcela=1,
        )

    def test_lista_despesas_filtra_por_status(self):
        response = self.client.get(reverse('despesas'), {'status': 'paga'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Conta paga')
        self.assertNotContains(response, 'Conta aberta')
        self.assertNotContains(response, 'Conta parcial')

    def test_lista_despesas_resumo_considera_pesquisa_sem_status(self):
        response = self.client.get(reverse('despesas'), {'search': 'Conta'})

        resumo = response.context['resumo_despesas']
        self.assertEqual(resumo['total'], 3)
        self.assertEqual(resumo['total_valor'], Decimal('600.00'))
        self.assertEqual(resumo['abertas'], 1)
        self.assertEqual(resumo['abertas_valor'], Decimal('100.00'))
        self.assertEqual(resumo['parciais'], 1)
        self.assertEqual(resumo['parciais_valor'], Decimal('200.00'))
        self.assertEqual(resumo['pagas'], 1)
        self.assertEqual(resumo['pagas_valor'], Decimal('300.00'))

    def test_pagamento_rapido_preenche_despesa_a_vista_com_data_e_valor_padrao(self):
        response = self.client.get(reverse('pagar_despesa', args=[self.aberta.id]))

        form = response.context['pagamento_form']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form['data_pagamento'].value(), date(2026, 5, 18))
        self.assertEqual(form['valor'].value(), Decimal('100.00'))
        self.assertEqual(form['numero_parcela'].value(), 1)

    def test_pagamento_rapido_preenche_proxima_parcela_pendente(self):
        self.parcial.data_primeiro_vencimento = date(2026, 6, 10)
        self.parcial.save(update_fields=['data_primeiro_vencimento'])
        self.parcial.gerar_parcelas_previstas()

        response = self.client.get(reverse('pagar_despesa', args=[self.parcial.id]))

        form = response.context['pagamento_form']
        parcela = response.context['parcela_selecionada']
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(parcela)
        self.assertEqual(parcela.numero_parcela, 1)
        self.assertEqual(form['parcela'].value(), parcela.id)
        self.assertEqual(form['data_pagamento'].value(), date(2026, 6, 10))
        self.assertEqual(form['valor'].value(), Decimal('100.00'))

    def test_pagamento_rapido_registra_pagamento_sem_abrir_edicao(self):
        response = self.client.post(
            reverse('pagar_despesa', args=[self.aberta.id]),
            {
                'data_pagamento': '2026-05-18',
                'valor': '100.00',
                'numero_parcela': '1',
                'observacao': 'Pagamento rapido',
            }
        )

        self.assertRedirects(response, reverse('despesas'))
        self.aberta.refresh_from_db()
        self.assertEqual(self.aberta.status, 'paga')
        self.assertEqual(self.aberta.pagamentos.count(), 1)
