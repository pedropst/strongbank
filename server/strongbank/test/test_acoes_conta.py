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
from rest_framework.authtoken.models import Token

payload = {
            "valor":100,
            "doc_destinatario":"11565662",
            "numero":"",
            "agencia":"",
            "senha":"123456"
          }

payload_incorreto = {
                        "valor":100,
                        "doc_destinatario":"11565662",
                        "numero":"",
                        "agencia":"",
                        "senha":"56155156"
                    }

class AcoesContaTestCase(TestCase):
    def setUp(self) -> None:
        self.client_auth = APIClient()
        User.objects.create(username="bianca", email="bianca@email.com", password="123456")
        self.owner1 = User.objects.get(username="bianca")
        self.owner1.set_password('123456')
        self.client_auth.login(username='bianca', password='123456')
        self.client_auth.force_authenticate(user=self.owner1)
        

        self.client_not_auth = APIClient()

        self.dados = ContaDadosSensiveis.objects.create(saldo=5000)

        Cliente.objects.create(nome="Bianca", endereco="Rua dos Moradores Bonitos 274", 
                        celular="1515", documento="118659326", tipo="PF",
                        dono=self.owner1)

        self.cliente1 = Cliente.objects.get(nome="Bianca")
        Conta.objects.create(cliente=self.cliente1, agencia="0001", dados_sensiveis=self.dados, tipo="PF")
        self.conta1 = Conta.objects.get(cliente=self.cliente1)


        User.objects.create(username="pedro", email="pedro@email.com", password="123456")
        self.owner2 = User.objects.get(username="pedro")

        Cliente.objects.create(nome="Pedro", endereco="Rua dos Moradores Bonitos 274", 
                celular="156156", documento="11565662", tipo="PF",
                dono=self.owner2)

        self.cliente2 = Cliente.objects.get(nome="Pedro")
        self.dados = ContaDadosSensiveis.objects.create(saldo=5000)
        Conta.objects.create(cliente=self.cliente2, agencia="0001", dados_sensiveis=self.dados, tipo="PF")
        self.conta2 = Conta.objects.get(cliente=self.cliente2)

    def test_transferir_de_cliente1_para_cliente2(self):
        payload['numero'] = self.conta2.numero
        payload['agencia'] = self.conta2.agencia

        response = self.client_auth.post('/transferir/', payload, format='json')

        self.assertEqual(response.status_code, 200)

    def test_transferir_de_cliente1_para_cliente2_verificar_se_saldo_foi_transferido(self):
        payload['numero'] = self.conta2.numero
        payload['agencia'] = self.conta2.agencia

        self.client_auth.post('/transferir/', payload, format='json')

        resultado = [self.conta1.saldo, self.conta2.saldo]
        self.assertEqual(resultado, [4900, 5100])
       
    def test_transferir_de_cliente1_para_cliente2_verificar_se_saldo_diminuiu_do_cliente1(self):
        payload['numero'] = self.conta2.numero
        payload['agencia'] = self.conta2.agencia

        self.client_auth.post('/transferir/', payload, format='json')

        self.assertEqual(self.conta1.saldo, 4900)
       
    def test_transferir_de_cliente1_para_cliente2_verificar_se_saldo_aumentou_do_cliente2(self):
        payload['numero'] = self.conta2.numero
        payload['agencia'] = self.conta2.agencia

        self.client_auth.post('/transferir/', payload, format='json')

        self.assertEqual(self.conta2.saldo, 5100)

    def test_transferir_de_cliente1_para_cliente2_senha_invalida(self):
        payload_incorreto['numero'] = self.conta2.numero
        payload_incorreto['agencia'] = self.conta2.agencia
        response = self.client_auth.post('/transferir/', payload_incorreto, format='json')

        self.assertEqual(response.status_code, 400)

    def test_retornar_saldo(self):
        response = self.client_auth.get('/saldo/', {}, format='json')

        self.assertEqual(response.json(), 5000)

    def test_retornar_saldo_apos_transferencia(self):
        payload['numero'] = self.conta2.numero
        payload['agencia'] = self.conta2.agencia

        self.client_auth.post('/transferir/', payload, format='json')

        response = self.client_auth.get('/saldo/', {}, format='json')

        self.assertEqual(response.json(), 4900)
    
    def test_retonar_200_quando_sacar(self):
        response = self.client_auth.post('/sacar/', {'valor':500, 'senha':123456}, format='json')

        self.assertEqual(response.status_code, 200)
    
    def test_diminuir_saldo_quando_sacado(self):
        self.client_auth.post('/sacar/', {'valor':500, 'senha':123456}, format='json')

        self.assertEqual(self.conta1.saldo, 4500)

    def test_aumentar_saldo_quando_sacado(self):
        self.client_auth.post('/depositar/', {'valor':500}, format='json')

        self.assertEqual(self.conta1.saldo, 5500)

    def test_retornar_400_quando_sacar_com_senha_errada(self):
        response = self.client_auth.post('/sacar/', {'valor':500, 'senha':153287}, format='json')

        self.assertEqual(response.status_code, 400)
    
    def test_retonar_200_quando_depositar(self):
        response = self.client_auth.post('/depositar/', {'valor':500}, format='json')

        self.assertEqual(response.status_code, 200)
    
    def test_retonar_200_quando_tirar_extrato(self):
        response = self.client_auth.post('/extrato/', {"dta_inicial":"09/07/2022", "dta_final":"13/07/2022"}, format='json')

        self.assertEqual(response.status_code, 200)
    
    def test_retonar_vazio_quando_tirar_extrato_sem_transacoes_previas(self):
        response = self.client_auth.post('/extrato/', {"dta_inicial":"09/07/2022", "dta_final":"13/07/2022"}, format='json')

        self.assertEqual(response.json(), [])
    
    def test_retonar_transacao_quando_tirar_extrato_com_transacao_previa(self):
        self.client_auth.post('/sacar/', {'valor':500, 'senha':123456}, format='json')
        response = self.client_auth.post('/extrato/', {"dta_inicial":"09/07/2022", "dta_final":"13/07/2022"}, format='json')

        self.assertEqual(len(response.json()), 1)
    
    def test_retonar_transacoes_quando_tirar_extrato_com_transacoes_previas(self):
        self.client_auth.post('/sacar/', {'valor':500, 'senha':123456}, format='json')
        self.client_auth.post('/depositar/', {'valor':500}, format='json')
        response = self.client_auth.post('/extrato/', {"dta_inicial":"09/07/2022", "dta_final":"13/07/2022"}, format='json')

        self.assertEqual(len(response.json()), 2)


        

    ## VALIDAR SE ESTÁ TENTANDO ENVIAR DE SI PARA SI MESMO NO TRANSFERENCIA SERIALIZER



        