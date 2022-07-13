import json
from django.test import TestCase
from rest_framework.test import APIClient
from strongbank.models.cliente import Cliente
from strongbank.models.conta import Conta, ContaDadosSensiveis
from strongbank.models.cartao import Cartao, CartaoDadosSensiveis
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import status
from strongbank.serializers.cliente_serializer import ClienteSerializer
from strongbank.serializers.conta_serializer import ContaSerializer
from django.contrib.auth.models import User
from rest_framework import exceptions


class CartaoTestCase(TestCase):
    def setUp(self) -> None:
        self.client_auth = APIClient()
        User.objects.create(username="bianca", email="bianca@email.com", password="123456")
        self.owner = User.objects.get(username="bianca")
        self.owner.is_superuser = False
        self.client_auth.force_authenticate(user=self.owner)

        self.client_not_auth = APIClient()

        Cliente.objects.create(nome="Bianca", endereco="Rua dos Moradores Bonitos 274", 
                               celular="1515", documento="1", tipo="PF",
                               dono=self.owner)

        self.cliente = Cliente.objects.get(nome="Bianca")

        dados_conta = ContaDadosSensiveis.objects.create(saldo=5000)
        self.conta = Conta.objects.create(cliente=self.cliente, agencia="0001", dados_sensiveis=dados_conta, tipo="P")

        self.dados = CartaoDadosSensiveis.objects.create(cvv="300")
    
    def test_cartao_buscar_antes_criar(self):
        with self.assertRaises(ObjectDoesNotExist):
            Cartao.objects.get(conta=self.conta)

    def test_cartao_criacao(self):
        cartao = Cartao.objects.create(conta=self.conta, dados_sensiveis=self.dados, dia_vencimento=15)

        self.assertEqual(type(cartao), Cartao)

    def test_cartao_criacao_por_requisicao(self):
        response = self.client_auth.post('/cartao/', {"dia_vencimento": "10", "limite_total":"1000"}, format='json')

        self.assertEqual(response.status_code, 201)

    def test_cartao_criacao_por_requisicao_com_payload_incorreto(self):
        response = self.client_auth.post('/cartao/', {"dia_vencimento": "10"}, format='json')

        self.assertEqual(response.status_code, 400)
        
    def test_cartao_criacao_dois_cartoes_pelo_mesmo_cliente(self):
        self.client_auth.post('/cartao/', {"dia_vencimento": "10", "limite_total":"1000"}, format='json')

        with self.assertRaises(IntegrityError):
            self.client_auth.post('/cartao/', {"dia_vencimento": "10", "limite_total":"1000"}, format='json')
    
    def test_cartao_verificar_limite_disponivel(self):
        self.client_auth.post('/cartao/', {"dia_vencimento": "10", "limite_total":"1000"}, format='json')
        cartao = Cartao.objects.get(conta=self.conta)

        self.assertEqual(cartao.limite_disponivel, 1000)
    
    def test_cartao_verificar_limite_desbloqueado(self):
        self.client_auth.post('/cartao/', {"dia_vencimento": "10", "limite_total":"1000"}, format='json')
        cartao = Cartao.objects.get(conta=self.conta)

        self.assertEqual(cartao.limite_desbloqueado, 800)