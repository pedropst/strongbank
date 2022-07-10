from datetime import datetime
from decimal import Decimal
from random import randint
from django.db import transaction
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework import permissions
from strongbank.models import Cliente, Conta, ContaDadosSensiveis, Transacao, Cartao, CartaoDadosSensiveis, Fatura, Parcela
from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers import ClienteSerializer, ContaSerializer, DepositarSerializer, ExtratoSerializer, SacarSerializer, SaldoSerializer, TransacaoSerializer, TransferirSerializer, UserSerializer, CartaoSerializer, FaturaSerializer, PagarCreditoSerializer, PagarDebitoSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import serializers

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        user = User.objects._create_user(request.data['username'], request.data['email'], request.data['senha'])
        user.is_superuser = True if request.data['tipo'] == 'A' else False
        user.save()
        return Response({'status': 'Usuário criado com sucesso!'}, status=201)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PagarCreditoViewset(viewsets.ViewSet):
    serializer_class = PagarCreditoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request):
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        cartao = Cartao.objects.filter(conta=conta).all().get(numeracao=request.data['numeracao'])
        faturas = Fatura.objects.filter(cartao=cartao).all()
        
        if len(faturas) > 0:
            faturas = sorted(faturas, key=lambda x: datetime(x.ano_ref, x.mes_ref, 1))

        faturas = [f for f in faturas if datetime(f.ano_ref, f.mes_ref, 1) >= datetime.today()]
        if request.data['parcelas'] > 12:
            pass #LEVANTAR ERRO (PROGRAMADOR NÃO TEVE TEMPO -> ESSE CARTÃO SÓ ACEITA EM ATÉ 12 VEZES)
        if cartao.pagar_credito(request.data['valor']):
            if len(faturas) == 0:
                for p in range(request.data['parcelas'] + 1)[1:]:
                    nova_fatura = Fatura.objects.create(mes_ref = datetime.today().month + p if datetime.today().month + p <= 12 else datetime.today().month + p - 12,
                                                        ano_ref = datetime.today().year if datetime.today().month + p <= 12 else datetime.today().year + 1,
                                                        total= Decimal(request.data['valor']/request.data['parcelas']),
                                                        parcial= Decimal(0),
                                                        cartao = cartao)
                    nova_parcela = Parcela.objects.create(fatura= nova_fatura,
                                        valor= Decimal(request.data['valor']/request.data['parcelas']),
                                        descricao= request.data['descricao'])
                    nova_fatura.save()
                    nova_parcela.save()
            elif len(faturas) <= request.data['parcelas']:
                for f in faturas:
                    nova_parcela = Parcela.objects.create(fatura= f,
                                                          valor= Decimal(request.data['valor']/request.data['parcelas']),
                                                          descricao= request.data['descricao'])
                    f.total += Decimal(request.data['valor']/request.data['parcelas'])
                    f.save()
                    nova_parcela.save()
                for p in range(request.data['parcelas'] + 1 - len(faturas))[1:]:
                    nova_fatura = Fatura.objects.create(mes_ref = datetime.today().month + p if datetime.today().month + p <= 12 else datetime.today().month + p - 12,
                                                        ano_ref = datetime.today().year if datetime.today().month + p <= 12 else datetime.today().year + 1,
                                                        total= Decimal(request.data['valor']/request.data['parcelas']),
                                                        parcial= Decimal(0),
                                                        cartao = cartao)
                    nova_parcela = Parcela.objects.create(fatura= nova_fatura,
                                                          valor= Decimal(request.data['valor']/request.data['parcelas']),
                                                          descricao= request.data['descricao'])
                    nova_fatura.save()
                    nova_parcela.save()

            return Response({'status': 'Pagamento realizado com sucesso!'}, status=200)
        else:
            return Response({'status': 'Pagamento NÃO realizado!'}, status=400)

class PagarDebitoViewset(viewsets.ViewSet):
    serializer_class = PagarDebitoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request):
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        cartao = Cartao.objects.filter(conta=conta).all().get(numeracao=request.data['numeracao'])

        if cartao.pagar_debito(request.data['valor'], conta):
            nova_transacao = Transacao.objects.create(tipo='PC',
                                                      cliente = cliente,
                                                      valor = request.data['valor'])
            nova_transacao.save()
        return Response({'status': 'Pagamento realizado com sucesso!'}, status=200)

class SacarViewset(viewsets.ViewSet):
    serializer_class = SacarSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request):
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)

        conta.sacar(request.data['valor'])
        nova_transacao = Transacao.objects.create(tipo='S',
                                                  cliente = cliente,
                                                  valor = request.data['valor'])
        nova_transacao.save()
        return Response({'status': 'Saque efetuado com sucesso!'}, status=200)

class SaldoViewset(viewsets.ViewSet):
    serializer_class = SaldoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # cliente = Cliente.objects.get(documento=request.data['documento'])
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        return Response({'Seu saldo é: ': conta.saldo}, status=200)

class ExtratoViewset(viewsets.ViewSet):
    serializer_class = ExtratoSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        transacoes = Transacao.objects.filter(cliente=cliente).all()
        extrato = conta.extrato(request.data['dta_inicial'], request.data['dta_final'], list(transacoes))
        # serializer = [ExtratoSerializer(x) for x in extrato]
        return Response(extrato, status=200)

class DepositarViewset(viewsets.ViewSet):
    serializer_class = DepositarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # cliente = Cliente.objects.get(documento=request.data['documento'])
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        
        nova_transacao = Transacao.objects.create(tipo='D',
                                    cliente = cliente,
                                    valor = request.data['valor'])
        nova_transacao.save()
        conta.depositar(request.data['valor'])
        return Response({'status': 'Depósito efetuado com sucesso!'}, status=200)
        # if AC.depositar(conta, request.data['valor']):
        #     return Response({'status': 'OK'}, status=200)


class TransferirViewset(viewsets.ViewSet):
    serializer_class = TransferirSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request):
        # cliente = Cliente.objects.get(dono=request.user)
        cliente_remetente = Cliente.objects.get(dono=request.user)
        # cliente_remetente = Cliente.objects.get(documento=request.data['doc_remetente'])
        conta_remetente = Conta.objects.get(cliente=cliente_remetente)

        cliente_destinatario = Cliente.objects.get(documento=request.data['doc_destinatario'])
        conta_destinatario = Conta.objects.get(cliente=cliente_destinatario, 
        numero=request.data['numero'],
        agencia=request.data['agencia'])

        conta_remetente.transferir(request.data['valor'], conta_destinatario)
        nova_transacao = Transacao.objects.create(tipo='TE',
                            cliente = cliente_remetente,
                            valor = request.data['valor'])
        nova_transacao.save()

        nova_transacao = Transacao.objects.create(tipo='TR',
                    cliente = cliente_destinatario,
                    valor = request.data['valor'])
        nova_transacao.save()
        return Response({'status': 'Transferência efetuada com sucesso!'}, status=200)
        # if AC.transferir(conta_remetente, request.data['valor'], conta_destinatario):
            # return Response({'status': 'OK'}, status=200)

class FaturaViewset(viewsets.ModelViewSet):
    serializer_class = FaturaSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request):
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        cartao = Cartao.objects.filter(conta=conta).all().get(numeracao=request.data['numeracao'])
        queryset =  Fatura.objects.filter(cartao=cartao).all()

        serializer = FaturaSerializer(queryset, many=True)
        return Response(serializer.data, status=200)


class ClienteViewset(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        clientes = Cliente.objects.all()
        return clientes

    def create(self, request, *args, **kwargs):
        novo_cliente = Cliente.objects.create(nome=request.data['nome'], 
                                              endereco=request.data['endereco'], 
                                              celular=request.data['celular'], 
                                              documento=request.data['cpf'] if request.data['tipo'] == 'PF' else request.data['cnpj'],
                                              dono=request.user)
        novo_cliente.save()

        serializer = ClienteSerializer(novo_cliente)
        return Response(serializer.data, status=201)

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = Cliente.objects.all()
            serializer = ClienteSerializer(queryset, many=True)
        else:
            queryset = Cliente.objects.get(dono=request.user)
            serializer = ClienteSerializer(queryset)
        return Response(serializer.data, status=200)

class ContaViewset(viewsets.ModelViewSet):
    serializer_class = ContaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contas = Conta.objects.all()
        return contas

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request, *args, **kwargs):
        cliente = Cliente.objects.get(dono=request.user)
        dados_sensiveis = request.data['dados_sensiveis']
        dados = ContaDadosSensiveis.objects.create(saldo=dados_sensiveis['saldo'])
        dados.save()

        nova_conta = Conta.objects.create(agencia=request.data['agencia'],
                                          tipo=request.data['tipo'], 
                                          cliente=cliente,
                                          dados_sensiveis=dados)
        nova_conta.save()

        serializer = ContaSerializer(nova_conta)

        return Response(serializer.data, status=201)

    def list(self, request, *args, **kwargs):
        cliente = Cliente.objects.get(dono=request.user)
        queryset = Conta.objects.get(cliente=cliente)
        if request.user.is_superuser:
            queryset = Conta.objects.all()
            serializer = ContaSerializer(queryset, many=True)
        else:
            serializer = ContaSerializer(queryset)
        return Response(serializer.data, status=200)


class CartaoViewset(viewsets.ModelViewSet):
    serializer_class = CartaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cartoes = Cartao.objects.all()
        return cartoes

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request, *args, **kwargs):
        if len(self.list(request, *args, **kwargs).data) <= 3:
            cliente = Cliente.objects.get(dono=request.user)
            conta = Conta.objects.get(cliente=cliente)
            dados = CartaoDadosSensiveis.objects.create(cvv=str(randint(100,999)))
            dados.save()

            nome_cliente = cliente.nome
            nomes = []
            if len(nome_cliente.split(' ')) == 2:
                nomes.append(nome_cliente.split(' ')[0])
                nomes.append(nome_cliente.split(' ')[1])
            else:
                nomes.append(nome_cliente.split(' ')[0])
                nomes.extend([n[0] for n in nome_cliente.split(' ')[1:-1]])
                nomes.append(nome_cliente.split(' ')[-1])

            nome = ''
            for n in nomes:
                nome += f'{n} '
            nome = nome[:-1]


            todos_numeros = [x.numeracao for x in list(Cartao.objects.all())]
            numeracao = '5431' + str(randint(10**11, (10**12)-1))
            while numeracao in todos_numeros :
                numeracao = '5431' + str(randint(10**11, (10**12)-1))

            novo_cartao = Cartao.objects.create(conta=conta,
                                                dia_vencimento=request.data['dia_vencimento'], 
                                                tipo=request.data['tipo'],
                                                dados_sensiveis=dados,
                                                nome=nome,
                                                numeracao=numeracao,
                                                limite_total=5000,
                                                limite_desbloqueado=3000,
                                                limite_disponivel=5000)
            novo_cartao.save()

            serializer = CartaoSerializer(novo_cartao)

            return Response(serializer.data, status=201)
        else:
            raise serializers.ValidationError(
                            {'Número máximo de cartão atingido':
                            'Cliente já possui 3 cartões.'})

    def list(self, request, *args, **kwargs):
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        queryset = Cartao.objects.filter(conta=conta).all()
        if request.user.is_superuser:
            queryset = Cartao.objects.all()
            serializer = CartaoSerializer(queryset, many=True)
        else:
            serializer = CartaoSerializer(queryset,  many=True)
        return Response(serializer.data, status=200)




