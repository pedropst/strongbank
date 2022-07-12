from django.test import TestCase
from rest_framework.test import APIClient
from strongbank.serializers.conta_serializer import ContaDadosSensiveisSerializer
from strongbank.models.cliente import Cliente
from strongbank.models.conta import ContaDadosSensiveis
from django.contrib.auth.models import User


class DadosContaTestCase(TestCase):
    def setUp(self) -> None:
        self.client_auth = APIClient()
        User.objects.create(username="bianca", email="bianca@email.com", password="123456")
        self.owner = User.objects.get(username="bianca")
        self.owner.is_superuser = False
        self.client_auth.force_authenticate(user=self.owner)

        Cliente.objects.create(nome="Bianca", endereco="Rua dos Moradores Bonitos 274", 
                               celular="1515", documento="1", tipo="PF",
                               dono=self.owner)

        self.cliente = Cliente.objects.get(nome="Bianca")


    def test_dados_conta_criacao(self):
        dados = ContaDadosSensiveis.objects.create(saldo=5000)

        self.assertEqual(type(dados), ContaDadosSensiveis)

    def test_dados_conta_atributo_saldo(self):
        dados = ContaDadosSensiveis.objects.create(saldo=5000)

        self.assertEqual(dados.saldo, 5000)

    def test_dados_conta_serializer_criacao(self):
        ContaDadosSensiveis.objects.create(saldo=5000)
        queryset = ContaDadosSensiveis.objects.get(saldo=5000)
        serializer = ContaDadosSensiveisSerializer(queryset)
        
        self.assertEqual(type(serializer), ContaDadosSensiveisSerializer)

    def test_dados_conta_serializer_fields(self):
        ContaDadosSensiveis.objects.create(saldo=5000)
        queryset = ContaDadosSensiveis.objects.get(saldo=5000)
        serializer = ContaDadosSensiveisSerializer(queryset)
        lista_fields = list(serializer.fields.keys())

        resultado = 0
        # resultado += 1 if 'id' in lista_fields else 0
        resultado += 1 if 'saldo' in lista_fields else 0
        resultado += 1 if len(lista_fields) == 1 else 0
        
        self.assertEqual(resultado, 2)