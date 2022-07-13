from dateutil import parser
from django.db import transaction
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from strongbank.models.cliente import Cliente
from strongbank.models.conta import Conta, ContaDadosSensiveis
from strongbank.models.transacao import Transacao
from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers.conta_serializer import ContaSerializer, DepositarSerializer, SacarSerializer, SaldoSerializer, TransferirSerializer
from strongbank.serializers.transacao_serializer import TransacaoSerializer

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
        if request.user.is_superuser:
            queryset = Conta.objects.all()
            serializer = ContaSerializer(queryset, many=True)
        else:
            cliente = Cliente.objects.get(dono=request.user)
            queryset = Conta.objects.get(cliente=cliente)
            serializer = ContaSerializer(queryset)
        return Response(serializer.data, status=200)


class SacarViewset(viewsets.ViewSet):
    serializer_class = SacarSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request):
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)

        serializer = SacarSerializer(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        if request.user.check_password(request.data['senha']):
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
        return Response(conta.saldo, status=200)


class ExtratoViewset(viewsets.ViewSet):
    serializer_class = TransacaoSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        transacoes = Transacao.objects.filter(cliente=cliente).all()
        extrato = conta.extrato(request.data['dta_inicial'], request.data['dta_final'], list(transacoes))
        serializer = TransacaoSerializer(extrato, many=True)
        return Response(serializer.data, status=200)


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
        cliente_remetente = Cliente.objects.get(dono=request.user)
        conta_remetente = Conta.objects.get(cliente=cliente_remetente)

        cliente_destinatario = Cliente.objects.get(documento=request.data['doc_destinatario'])
        conta_destinatario = Conta.objects.get(cliente=cliente_destinatario, 
                                               numero=request.data['numero'],
                                               agencia=request.data['agencia'])

        serializer = TransferirSerializer(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)

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

            