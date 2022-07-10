from rest_framework import viewsets
from rest_framework.response import Response

from strongbank.models.cartao import Cartao
from strongbank.models.cliente import Cliente
from strongbank.models.conta import Conta
from strongbank.models.fatura import Fatura
from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers.fatura_serializer import FaturaSerializer


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

        