from datetime import datetime
from decimal import Decimal
from django.db import transaction
from random import randint
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.response import Response

from strongbank.models.cartao import Cartao, CartaoDadosSensiveis
from strongbank.models.cliente import Cliente
from strongbank.models.conta import Conta
from strongbank.models.fatura import Fatura
from strongbank.models.parcela import Parcela
from strongbank.models.transacao import Transacao
from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers.cartao_serializer import  CartaoSerializer, PagarCreditoSerializer, PagarDebitoSerializer


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
