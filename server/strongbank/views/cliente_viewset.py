from django.db import transaction
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from strongbank.models.cliente import Cliente
from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers.cliente_serializer import ClienteSerializer
from rest_framework import status

class ClienteViewset(viewsets.ModelViewSet):
    """
        Classe reponsável por implementar o endpoint do cliente. 
        Esse endpoint requer autenticação para acessá-lo.
    """

    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer    
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    @transaction.atomic # To create either BOTH or NONE
    def create(self, request):
        """
            Método responsável pela criação de um cliente.
        """

        request.data['documento'] = request.data['cpf'] if request.data['tipo'] == 'PF' else request.data['cnpj']
        serializer = ClienteSerializer(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        
        novo_cliente = Cliente.objects.create(nome=request.data['nome'], 
                                        endereco=request.data['endereco'], 
                                        celular=request.data['celular'], 
                                        documento=request.data['cpf'] if request.data['tipo'] == 'PF' else request.data['cnpj'],
                                        tipo=request.data['tipo'],
                                        dono=request.user)
        novo_cliente.save()

        return Response(serializer.data, status=201)

    def list(self, request):
        """
            Método que retorna informações sobre o cliente para um usuário comum,
            e sobre todas os clientes para um usuário administrador.
        """

        if request.user.is_superuser:
            queryset = Cliente.objects.all()
            serializer = ClienteSerializer(queryset, many=True)
        else:
            queryset = Cliente.objects.get(dono=request.user)
            serializer = ClienteSerializer(queryset)
        return Response(serializer.data, status=200)
