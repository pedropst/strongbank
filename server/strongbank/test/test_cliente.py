import json
from django.test import TestCase
from rest_framework.test import APIClient
from strongbank.models.cliente import Cliente
from rest_framework import status
from strongbank.serializers.cliente_serializer import ClienteSerializer
from django.contrib.auth.models import User

payloadPF = {
                "nome": "Bianca dos Santos",
                "endereco": "Rua dos Moradores Bonitos, 274",
                "celular": "1234567891123",
                "cpf": "15676456212",
                "cnpj": "",
                "tipo": "PF"
            }

payloadPJ = {
                "nome": "Bipe Lab Criativo",
                "endereco": "Rua dos Moradores Bonitos, 274",
                "celular": "1234567891123",
                "cpf": "15676456210",
                "cnpj": "12345678911234",
                "tipo": "PJ"
            }

class ClienteTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        User.objects.create(username="bianca", email="bianca@email.com", password="123456")
        self.owner = User.objects.get(username="bianca")
        self.owner.is_superuser = False
        self.client.force_authenticate(user=self.owner)

    def test_cliente_criacao(self):
        Cliente.objects.create(nome="Bianca", endereco="Rua dos Moradores Bonitos 274", 
                               celular="1515", documento="1", tipo="PF",
                               dono=self.owner)

        cliente = Cliente.objects.get(nome="Bianca")

        self.assertEqual(cliente.nome, "Bianca")

    def test_cliente_criacao_PF_por_request(self):
        response = self.client.post('/cliente/', payloadPF, format='json')

        self.assertEqual(response.status_code, 201)

    def test_cliente_criacao_PJ_por_request(self):
        response = self.client.post('/cliente/', payloadPJ, format='json')

        self.assertEqual(response.status_code, 201)

    def test_listar_cliente_como_usuario_normal(self):
        self.client.post('/cliente/', payloadPF, format='json')
        response = self.client.get('/cliente/')

        self.assertEqual(type(response.json()), dict)

    def test_listar_cliente_como_usuario_admin(self):
        self.owner.is_superuser = True
        self.client.post('/cliente/', payloadPF, format='json')
        response = self.client.get('/cliente/')

        self.assertEqual(type(response.json()), list)