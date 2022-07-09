from django.db import transaction
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework import permissions
from strongbank.models import Cliente, Conta, ContaDadosSensiveis, Transacao
from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers import ClienteSerializer, ContaSerializer, DepositarSerializer, ExtratoSerializer, SacarSerializer, SaldoSerializer, TransacaoSerializer, TransferirSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics

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

class SacarViewSet(viewsets.ViewSet):
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

class SaldoViewSet(viewsets.ViewSet):
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

class DepositarViewSet(viewsets.ViewSet):
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

class TransferirViewSet(viewsets.ViewSet):
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


class ClienteViewSet(viewsets.ModelViewSet):
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
        queryset = Cliente.objects.get(dono=request.user)
        if request.user.is_superuser:
            queryset = Cliente.objects.all()
            serializer = ClienteSerializer(queryset, many=True)
        else:
            serializer = ClienteSerializer(queryset)
        return Response(serializer.data, status=200)

class ContaViewSet(viewsets.ModelViewSet):
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
