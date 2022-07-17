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
from strongbank.serializers.cartao_serializer import  CartaoSerializer, PagarCreditoSerializer, PagarDebitoSerializer, AlterarBloqueioSerializer


class PagarCreditoViewset(viewsets.ViewSet):
    """
        Classe reponsável por implementar o endpoint do pagamento por crédito.
        Esse endpoint requer autenticação do dono para acessá-lo.
    """
    serializer_class = PagarCreditoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request):
        """
            Método responsável pela "criação" de um pagamento por crédito. Para 
            isso é necessário ter o valor e a quantidade de parcelas.
        """
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        cartao = Cartao.objects.get(conta=conta)
        faturas = Fatura.objects.filter(cartao=cartao).all()

        serializer = PagarCreditoSerializer(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        
        if len(faturas) > 0:
            faturas = sorted(faturas, key=lambda x: datetime(x.ano_ref, x.mes_ref, 1))

        faturas = [f for f in faturas if datetime(f.ano_ref, f.mes_ref, 1) >= datetime.today()]

        if cartao.pagar_credito(request.data['valor']):
            if not len(faturas):
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
                    nova_fatura = Fatura.objects.create(mes_ref = datetime.today().month + p + len(faturas) if datetime.today().month + p + len(faturas) <= 12 else datetime.today().month + p - 12 + len(faturas),
                                                        ano_ref = datetime.today().year if datetime.today().month + p + len(faturas) <= 12 else datetime.today().year + 1,
                                                        total= Decimal(request.data['valor']/request.data['parcelas']),
                                                        parcial= Decimal(0),
                                                        cartao = cartao)
                    nova_parcela = Parcela.objects.create(fatura= nova_fatura,
                                                          valor= Decimal(request.data['valor']/request.data['parcelas']),
                                                          descricao= request.data['descricao'])
                    nova_fatura.save()
                    nova_parcela.save()
            else:
                for p in range(request.data['parcelas'] + 1)[1:]:
                    nova_parcela = Parcela.objects.create(fatura= faturas[p-1],
                                                          valor= Decimal(request.data['valor']/request.data['parcelas']),
                                                          descricao= request.data['descricao'])
                    nova_parcela.save()

            return Response({'status': 'Pagamento realizado com sucesso!'}, status=200)
        else:
            return Response({'status': 'Pagamento NÃO realizado!'}, status=400)


class PagarDebitoViewset(viewsets.ViewSet):
    """
        Classe reponsável por implementar o endpoint do pagamento por débito.
        Esse endpoint requer autenticação do dono para acessá-lo.
    """
    serializer_class = PagarDebitoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request):
        """
            Método responsável pela "criação" de um pagamento por débito. Para 
            isso é necessário ter o valor e a quantidade de parcelas.
        """

        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        cartao = Cartao.objects.get(conta=conta)

        serializer = PagarDebitoSerializer(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        
        if len(request.data) != 2:
            raise serializers.ValidationError({"ERRO":"Payload INVÁLIDO."}, code=400)
        if cartao.pagar_debito(request.data['valor'], conta):
            nova_transacao = Transacao.objects.create(tipo='PC',
                                                      cliente = cliente,
                                                      valor = request.data['valor'],
                                                      descricao = request.data['descricao'])
            nova_transacao.save()
        return Response({'status': 'Pagamento realizado com sucesso!'}, status=200)

class AlterarBloqueioViewset(viewsets.ViewSet):
    """
        Classe reponsável por implementar o endpoint do bloqueio ou desbloqueio
        do cartão. Esse endpoint requer autenticação do dono para acessá-lo.
    """
    serializer_class = AlterarBloqueioSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request):
        """
            Método responsável pela "criação" de um bloqueio do cartão ou desbloqueio.
            Para isso é necessário ter o valor e a quantidade de parcelas.
        """

        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        cartao = Cartao.objects.get(conta=conta)

        estado_atual = cartao.bloqueado
        cartao.inverter_estado_bloqueio()

        if estado_atual:
            return Response({'status': 'Cartão desbloqueado com sucesso!'}, status=200)
        else:
            return Response({'status': 'Cartão bloqueado com sucesso!'}, status=200)
    
    def list(self, request):
        """
            Método que retorna informações sobre o bloqueio do cartão para o dono.
        """
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        cartao = Cartao.objects.get(conta=conta)
        return Response(cartao.bloqueado, status=200)

class CartaoViewset(viewsets.ModelViewSet):
    """
        Classe reponsável por implementar o endpoint do cartão. 
        Esse endpoint requer autenticação para acessá-lo.
    """
    serializer_class = CartaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    # TODO Verificar se não é necessário fazer partial update para salvar o valor da fatura do cartão
    # quando a mesma já existe, mas foi aumentada por conta de uma nova parcela.
    def get_queryset(self):
        cartoes = Cartao.objects.all()
        return cartoes

    # def partial_update(self, request, *args, **kwargs):
    #     if request.user.is_superuser:
    #         pass # ERROR SUPER USER NOT SUPPOSE TO CHANGE CARD INFO
    #     else:
    #         cliente = Cliente.objects.get(dono=request.user)
    #         conta = Conta.objects.get(cliente=cliente)
    #         cartao = Cartao.objects.get(conta=conta)
    #         cartao.bloqueado = True if request.data['bloqueado'] == 1 else False
    #         cartao.limite_desbloqueado = request.data['limite_desbloqueado'] if request.data['limite_desbloqueado'] < cartao.limite_disponivel else cartao.limite_desbloqueado
    #         cartao.save()
    #     return Response({"status":"Cartão bloqueado com sucesso!"}, status=200)

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request, *args, **kwargs):
        """
            Método responsável pela criação de um cartão. A criação do dados
            sensíveis de um cartão (cvv), também é criado e validado aqui antes
            de criar o cartão.
        """

        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        dados = CartaoDadosSensiveis.objects.create(cvv=str(randint(100,999)))
        dados.save()

        nome = ''
        nome_cliente = cliente.nome
        nomes_separados = nome_cliente.split(' ')
        nomes = []

        if len(nomes_separados) == 2:
            nome = nome_cliente
        else:
            nomes.append(nome_cliente.split(' ')[0])
            nomes.extend([n[0] for n in nome_cliente.split(' ')[1:-1]])
            nomes.append(nome_cliente.split(' ')[-1])
            
        for n in nomes:
            nome += f'{n} '
        if nome[-1] == " ":
            nome = nome[:-1]

        todos_numeros = [x.numeracao for x in list(Cartao.objects.all())]
        numeracao = '5431' + str(randint(10**11, (10**12)-1))
        while numeracao in todos_numeros :
            numeracao = '5431' + str(randint(10**11, (10**12)-1))

        
        if 'dia_vencimento' not in (request.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "dia_vencimento" não informado.'}, code=400)
        elif 'limite_total' not in (request.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "limite_total" não informado.'}, code=400)

        novo_cartao = Cartao.objects.create(conta=conta,
                                            dia_vencimento=request.data['dia_vencimento'], 
                                            dados_sensiveis=dados,
                                            nome=nome,
                                            numeracao=numeracao,
                                            limite_total=Decimal(request.data['limite_total']),
                                            limite_desbloqueado=Decimal(request.data['limite_total'])*Decimal(0.8),
                                            limite_disponivel=Decimal(request.data['limite_total']))

        request.data['dados_sensiveis'] = dados
        request.data['nome'] = nome
        request.data['numeracao'] = numeracao
        request.data['limite_total'] = Decimal(request.data['limite_total'])
        request.data['limite_desbloqueado'] = Decimal(request.data['limite_total'])*Decimal(0.8)
        request.data['limite_desbloqueado'] = Decimal(request.data['limite_total'])

        serializer = CartaoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        novo_cartao.save()

        serializer = CartaoSerializer(novo_cartao)

        return Response(serializer.data, status=201)

    def list(self, request):
        """
            Método que retorna informações sobre o cartão para um usuário comum,
            e sobre todas os cartões para um usuário administrador.
        """
        
        if request.user.is_superuser:
            queryset = Cartao.objects.all()
            serializer = CartaoSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            cliente = Cliente.objects.get(dono=request.user)
            conta = Conta.objects.get(cliente=cliente)
            queryset = Cartao.objects.get(conta=conta)
            serializer = CartaoSerializer(queryset)
            cartao = dict(serializer.data)
            cartao.pop('id')
            return Response(cartao, status=200)
