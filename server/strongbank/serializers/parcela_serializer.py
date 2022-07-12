from rest_framework import serializers

from strongbank.models.parcela import Parcela


class ParcelaSerializer(serializers.ModelSerializer):
    fatura = serializers.ReadOnlyField(source='fatura.id')
    class Meta:
        model = Parcela
        fields = ['id', 'fatura', 'descricao', 'valor', 'dta_criacao']
        depth = 1

        