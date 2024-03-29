from rest_framework import viewsets
from rest_framework.response import Response

from strongbank.models.cartao import Cartao
from strongbank.models.cliente import Cliente
from strongbank.models.conta import Conta
from strongbank.models.fatura import Fatura
from strongbank.models.parcela import Parcela
from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers.fatura_serializer import FaturaSerializer
from strongbank.serializers.parcela_serializer import ParcelaSerializer


class FaturaViewset(viewsets.ModelViewSet):
    """
        Classe reponsável por implementar da parcela. Essa classe é somente acessada
        pela classe de pagamento por meio de cartão de crédito.
    """

    serializer_class = ParcelaSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request):
        """
            Método que retorna informações sobre a fatura para um usuário comum,
            e sobre todas as faturas para um usuário administrador.
        """

        cliente = Cliente.objects.get(dono=request.user)
        conta = Conta.objects.get(cliente=cliente)
        cartao = Cartao.objects.get(conta=conta)
        fatura =  Fatura.objects.filter(cartao=cartao).all()
        parcela = Parcela.objects.all()

        serializer = FaturaSerializer(fatura, many=True)
        serializer2 = ParcelaSerializer(parcela, many=True)
        return Response({'FATURAS': serializer.data, 'PARCELAS': serializer2.data}, status=200)

        