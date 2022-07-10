from rest_framework import serializers

from strongbank.models.cartao import Cartao, CartaoDadosSensiveis


class CartaoDadosSensiveisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaoDadosSensiveis
        fields = ['id', 'cvv']


class CartaoSerializer(serializers.ModelSerializer):
    cvv = serializers.ReadOnlyField(source='dados_sensiveis.cvv')

    class Meta:
        model = Cartao
        fields = ['nome', 'numeracao', 'mes_validade', 'ano_validade', 'cvv', 'limite_total', 'limite_desbloqueado']


class PagarCreditoSerializer(serializers.Serializer):
    class Meta:
        fields = ['valor', 'parcelas']


class PagarDebitoSerializer(serializers.Serializer):
    class Meta:
        fields = ['valor']

