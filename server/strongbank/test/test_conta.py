import json
from django.test import TestCase
from rest_framework.test import APIClient
from strongbank.models.cliente import Cliente
from strongbank.models.conta import Conta, ContaDadosSensiveis
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import status
from strongbank.serializers.cliente_serializer import ClienteSerializer
from strongbank.serializers.conta_serializer import ContaSerializer
from django.contrib.auth.models import User
from rest_framework import exceptions

payload = {
              "agencia": "0010",
              "dados_sensiveis":{
                                    "saldo":150000
                                },
              "tipo":"P"
          }

class ContaTestCase(TestCase):
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

        self.dados = ContaDadosSensiveis.objects.create(saldo=5000)


    def test_conta_buscar_antes_criar(self):
        with self.assertRaises(ObjectDoesNotExist):
            Conta.objects.get(cliente=self.cliente)

    def test_conta_criacao(self):
        Conta.objects.create(cliente=self.cliente, agencia="0001", dados_sensiveis=self.dados, tipo="PF")
        conta = Conta.objects.get(cliente=self.cliente)

        self.assertEqual(type(conta), Conta)

    def test_conta_criacao_por_request(self):
        response = self.client_auth.post('/conta/', payload, format='json')

        self.assertEqual(response.status_code, 201)

    def test_conta_criacao_duas_contas_mesmo_cliente(self):
        self.client_auth.post('/conta/', payload, format='json')

        with self.assertRaises(IntegrityError):
            self.client_auth.post('/conta/', payload, format='json')
        
    def test_conta_geracao_numero_de_conta_criado(self):
        self.client_auth.post('/conta/', payload, format='json')
        conta = Conta.objects.get(cliente=self.cliente)

        self.assertNotEqual(conta.numero, "")

    def test_conta_geracao_numero_de_conta_com_len_igual_6(self):
        self.client_auth.post('/conta/', payload, format='json')
        conta = Conta.objects.get(cliente=self.cliente)

        self.assertEqual(len(conta.numero), 6)

    def test_conta_atributo_tipo(self):
        self.client_auth.post('/conta/', payload, format='json')
        conta = Conta.objects.get(cliente=self.cliente)

        self.assertEqual(conta.tipo, "P")

    def test_conta_atributo_cliente(self):
        self.client_auth.post('/conta/', payload, format='json')
        conta = Conta.objects.get(cliente=self.cliente)

        self.assertEqual(conta.cliente.nome, self.cliente.nome)

    def test_conta_atributo_agencia(self):
        self.client_auth.post('/conta/', payload, format='json')
        conta = Conta.objects.get(cliente=self.cliente)

        self.assertEqual(conta.agencia, "0010")

    def test_conta_atributo_dados_sensiveis(self):
        self.client_auth.post('/conta/', payload, format='json')
        conta = Conta.objects.get(cliente=self.cliente)

        self.assertEqual(conta.dados_sensiveis.saldo, 150000)

    def test_conta_sem_autenticacao(self):
        response = self.client_not_auth.post('/conta/', payload, format='json')
        self.assertEqual(response.status_code, 403)

    def test_conta_serializer_criacao(self):
        self.client_auth.post('/conta/', payload, format='json')
        queryset = Conta.objects.get(cliente=self.cliente)
        serializer = ContaSerializer(queryset)
        
        self.assertEqual(type(serializer), ContaSerializer)

    def test_conta_serializer_fields(self):
        self.client_auth.post('/conta/', payload, format='json')
        queryset = Conta.objects.get(cliente=self.cliente)
        serializer = ContaSerializer(queryset)
        lista_fields = list(serializer.fields.keys())

        resultado = 0
        resultado += 1 if 'cliente' in lista_fields else 0
        resultado += 1 if 'agencia' in lista_fields else 0
        resultado += 1 if 'numero' in lista_fields else 0
        resultado += 1 if 'tipo' in lista_fields else 0
        resultado += 1 if len(lista_fields) == 5 else 0
        
        self.assertEqual(resultado, 5)