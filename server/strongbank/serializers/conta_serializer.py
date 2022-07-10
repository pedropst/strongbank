from rest_framework import serializers

from strongbank.models.conta import Conta, ContaDadosSensiveis


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['id', 'cliente', 'agencia', 'numero', 'tipo']


class ContaDadosSensiveisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaDadosSensiveis
        fields = ['id', 'saldo']


class TransferirSerializer(serializers.Serializer):
    class Meta:
        fields = ['doc_remetente', 'valor', 'doc_destinatario']


class SacarSerializer(serializers.Serializer):
    class Meta:
        fields = ['documento', 'valor']


class DepositarSerializer(serializers.Serializer):
    class Meta:
        fields = ['documento', 'valor']


class SaldoSerializer(serializers.Serializer):
    class Meta:
        fields = ['documento']


class ExtratoSerializer(serializers.Serializer):
    class Meta:
        fields = ['data_inicial', 'data_final']

