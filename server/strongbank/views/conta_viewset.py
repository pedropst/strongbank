from dateutil import parser
from django.db import transaction
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from strongbank.models.cliente import Cliente
from strongbank.models.conta import Conta, ContaDadosSensiveis
from strongbank.models.transacao import Transacao
from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers.cliente_serializer import ClienteSerializer
from strongbank.serializers.conta_serializer import ContaSerializer, ContaDadosSensiveisSerializer, DepositarSerializer, SacarSerializer, SaldoSerializer, TransferirSerializer
from strongbank.serializers.transacao_serializer import TransacaoSerializer

class ContaViewset(viewsets.ModelViewSet):
    """
        Classe reponsável por implementar a view do endpoint da conta. Para esse 
        endpoint é necessário autenticação para acessá-lo.
    """
    serializer_class = ContaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contas = Conta.objects.all()
        return contas

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request, *args, **kwargs):
        """
            Método responsável pela criação de uma conta. A criação do dados
            sensíveis de uma conta (saldo), também é criado e validado aqui antes
            de criar a conta.
        """
        cliente = Cliente.objects.filter(dono=request.user).all()[0]
        dados_sensiveis = request.data['dados_sensiveis']

        serializer = ContaDadosSensiveisSerializer(data=dados_sensiveis)
        serializer.is_valid(raise_exception=True)

        dados = ContaDadosSensiveis.objects.create(saldo=dados_sensiveis['saldo'])
        dados.save()

        request.data['dados_sensiveis'] = dados
        # request.data['cliente'] = cliente
        request.data['cliente'] = {'nome': cliente.nome, 'endereco': cliente.endereco,
                                   'celular': cliente.celular, 'documento': cliente.documento,
                                   'tipo': cliente.tipo}

        serializer = ContaSerializer(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)

        nova_conta = Conta.objects.create(agencia=request.data['agencia'],
                                          tipo=request.data['tipo'], 
                                          cliente=cliente,
                                          dados_sensiveis=dados)
        nova_conta.save()


        return Response(serializer.data, status=201)

    def list(self, request, *args, **kwargs):
        """
            Método que retorna informações sobre a conta para um usuário comum,
            e sobre todas as contas para um usuário administrador.
        """
        if request.user.is_superuser:
            queryset = Conta.objects.all()
            serializer = ContaSerializer(queryset, many=True)
        else:
            cliente = Cliente.objects.get(dono=request.user)
            queryset = Conta.objects.get(cliente=cliente)
            serializer = ContaSerializer(queryset)
        return Response(serializer.data, status=200)

class SacarViewset(viewsets.ViewSet):
    """
        Classe reponsável por implementar a view do endpoint do saque. Para esse 
        endpoint é necessário autenticação e ser o dono da conta para acessá-lo.
        Portanto, usuários comuns que podem usar saque, já administradores não.
    """
    serializer_class = SacarSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request):
        """
            Método responsável pela "criação" de um saque. Para isso é  necessário 
            ter o valor, opcionalmente uma descrição e uma senha. Esse método 
            também possui a lógica registrar uma transação referente ao depósito e
            verifica a validação dos dados necessários para o saque.
        """
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)

        serializer = SacarSerializer(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)

        # if request.user.check_password(request.data['senha']):
        conta.sacar(request.data['valor'])

        nova_transacao = Transacao.objects.create(tipo='S',
                                                  cliente = cliente,
                                                  valor = request.data['valor'],
                                                  descricao = request.data['descricao'])
        nova_transacao.save()
          
        return Response({'status': 'Saque efetuado com sucesso!'}, status=200)

class SaldoViewset(viewsets.ViewSet):
    """
        Classe reponsável por implementar a view do endpoint do saldo. Para esse 
        endpoint é necessário autenticação e ser o dono da conta para acessá-lo.
        Portanto, usuários comuns que podem usar saldo, já administradores não.
    """

    serializer_class = SaldoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request):
        """
            Método responsável pela envio do saldo quando requisitado.
        """
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        return Response(conta.saldo, status=200)

class ExtratoViewset(viewsets.ViewSet):
    """
        Classe reponsável por implementar a view do endpoint do extrato. Para esse 
        endpoint é necessário autenticação e ser o dono da conta para acessá-lo.
        Portanto, usuários comuns que podem usar extrato, já administradores não.
    """

    serializer_class = TransacaoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        """
            Método responsável pela envio de um extrato. Para isso é  necessário 
            ter a data inicial e final.
        """

        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        transacoes = Transacao.objects.filter(cliente=cliente).all()
        extrato = conta.extrato(request.data['dta_inicial'], request.data['dta_final'], list(transacoes))
        serializer = TransacaoSerializer(extrato, many=True)
        return Response(serializer.data, status=200)

class DepositarViewset(viewsets.ViewSet):
    """
        Classe reponsável por implementar a view do endpoint do depósito. Para esse 
        endpoint é necessário autenticação e ser o dono da conta para acessá-lo.
        Portanto, usuários comuns que podem usar depósito, já administradores não.
    """

    serializer_class = DepositarSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        """
            Método responsável pela "criação" de um depósito. Para isso é
            necessário ter o valor e opcionalmente uma descrição. Esse método 
            também possui a lógica registrar uma transação referente ao depósito.
        """
        
        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        
        # TODO Validar depósito serializer antes de criar nova_transacao.
        nova_transacao = Transacao.objects.create(tipo='D',
                                                  cliente = cliente,
                                                  valor = request.data['valor'],
                                                  descricao = request.data['descricao'])
        nova_transacao.save()

        serializer = DepositarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conta.depositar(request.data['valor'])
        
        return Response({'status': 'Depósito efetuado com sucesso!'}, status=200)

class TransferirViewset(viewsets.ViewSet):
    """
        Classe reponsável por implementar a view do endpoint da transferência. Para esse 
        endpoint é necessário autenticação e ser o dono da conta para acessá-lo.
        Portanto, usuários comuns que podem usar transferência, já administradores não.
    """
    
    serializer_class = TransferirSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @transaction.atomic # To create either BOTH or NONE
    def create(self, request):
        """
            Método responsável pela "criação" de uma transferência. Para isso é
            necessário ter o número, agência e documento da conta destinatária.
            Esse método também possui a lógica para determinar quem é o remetente,
            valida os dados da transferência e registra em duas transações a trans-
            ferência, remetendo como transf. efetuada, e destinatário como transf.
            recebida.
        """

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
            