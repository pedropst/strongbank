from django.test import TestCase
from rest_framework.test import APIClient
from strongbank.models.cliente import Cliente
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

incorrect_payload = {
                        "nome": "Bipe Lab Criativo",
                        "endereco": "Rua dos Moradores Bonitos, 274",
                        "celular": "1234567891123",
                        "cpf": "15676456210",
                        "cnpj": "12345678911234"
                    }

class ClienteTestCase(TestCase):
    def setUp(self) -> None:
        self.client_auth = APIClient()
        User.objects.create(username="bianca", email="bianca@email.com", password="123456")
        self.owner = User.objects.get(username="bianca")
        self.owner.is_superuser = False
        self.client_auth.force_authenticate(user=self.owner)

        self.client_not_auth = APIClient()

    def test_cliente_criacao(self):
        Cliente.objects.create(nome="Bianca", endereco="Rua dos Moradores Bonitos 274", 
                               celular="1515", documento="1", tipo="PF",
                               dono=self.owner)

        cliente = Cliente.objects.get(nome="Bianca")

        self.assertEqual(type(cliente), Cliente)

    def test_cliente_criacao_PF_por_request(self):
        response = self.client_auth.post('/cliente/', payloadPF, format='json')

        self.assertEqual(response.status_code, 201)

    def test_cliente_atributo_nome(self):
        self.client_auth.post('/cliente/', payloadPF, format='json')
        cliente = Cliente.objects.get(documento="15676456212")

        self.assertEqual(cliente.nome, "Bianca dos Santos")

    def test_cliente_atributo_endereco(self):
        self.client_auth.post('/cliente/', payloadPF, format='json')
        cliente = Cliente.objects.get(documento="15676456212")

        self.assertEqual(cliente.endereco, "Rua dos Moradores Bonitos, 274")

    def test_cliente_atributo_celular(self):
        self.client_auth.post('/cliente/', payloadPF, format='json')
        cliente = Cliente.objects.get(documento="15676456212")

        self.assertEqual(cliente.celular, "1234567891123")

    def test_cliente_atributo_tipo(self):
        self.client_auth.post('/cliente/', payloadPF, format='json')
        cliente = Cliente.objects.get(documento="15676456212")

        self.assertEqual(cliente.tipo, "PF")

    def test_cliente_criacao_PJ_por_request(self):
        response = self.client_auth.post('/cliente/', payloadPJ, format='json')

        self.assertEqual(response.status_code, 201)

    def test_listar_cliente_como_usuario_normal(self):
        self.client_auth.post('/cliente/', payloadPF, format='json')
        response = self.client_auth.get('/cliente/')

        self.assertEqual(type(response.json()), dict)

    def test_listar_cliente_como_usuario_admin(self):
        self.owner.is_superuser = True
        self.client_auth.post('/cliente/', payloadPF, format='json')
        response = self.client_auth.get('/cliente/')

        self.assertEqual(type(response.json()), list)

    def test_cliente_criacao_errada_tipo(self):
        with self.assertRaises(KeyError):
            self.client_auth.post('/cliente/', incorrect_payload, format='json')

    def test_cliente_sem_autenticacao(self):
        response = self.client_not_auth.post('/cliente/', payloadPF, format='json')
        self.assertEqual(response.status_code, 403)

    def test_conta_serializer_fields(self):
        self.client_auth.post('/cliente/', payloadPF, format='json')
        queryset = Cliente.objects.get(documento="15676456212")
        serializer = ClienteSerializer(queryset)
        lista_fields = list(serializer.fields.keys())

        resultado = 0
        resultado += 1 if 'nome' in lista_fields else 0
        resultado += 1 if 'endereco' in lista_fields else 0
        resultado += 1 if 'celular' in lista_fields else 0
        resultado += 1 if 'documento' in lista_fields else 0
        resultado += 1 if 'tipo' in lista_fields else 0
        resultado += 1 if len(lista_fields) == 5 else 0
        
        self.assertEqual(resultado, 6)

