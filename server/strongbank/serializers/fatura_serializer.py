from rest_framework import serializers

from strongbank.models.fatura import Fatura


class FaturaSerializer(serializers.ModelSerializer):
    """
        Classe responsável pela serialização e deserialização das faturas.
    """
    cartao = serializers.ReadOnlyField(source='cartao.id')
    class Meta:
        model = Fatura
        fields = ['id', 'cartao', 'mes_ref', 'ano_ref', 'total', 'parcial']
