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


payloadC = {
	"valor": 42.87,
	"parcelas": 5,
	"descricao": "Teste"
}

payloadD = {
	"valor": 50,
	"descricao": "Teste"
}

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
        self.client_auth.post('/cartao/', {"dia_vencimento": "10", "limite_total":"1000"}, format='json')

    def test_acao_cartao_pagar_com_credito(self):
        response = self.client_auth.post('/pagarcredito/', payloadC, format='json')

        self.assertEqual(response.status_code, 200)

    def test_acao_cartao_pagar_com_debito(self):
        response = self.client_auth.post('/pagardebito/', payloadD, format='json')

        self.assertEqual(response.status_code, 200)

    def test_acao_cartao_pagar_com_credito_payload_incorreto(self):
        response = self.client_auth.post('/pagarcredito/', payloadD, format='json')

        self.assertEqual(response.status_code, 400)

    def test_acao_cartao_pagar_com_debito_payload_incorreto(self):
        response = self.client_auth.post('/pagardebito/', payloadC, format='json')

        self.assertEqual(response.status_code, 400)
    