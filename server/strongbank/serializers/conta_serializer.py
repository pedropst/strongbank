from random import randint
from rest_framework import serializers
from strongbank.serializers.cliente_serializer import ClienteSerializer
from strongbank.models.cliente import Cliente

from strongbank.models.conta import Conta, ContaDadosSensiveis

"""
"Each field in a Form class is responsible not only for validating data, 
but also for "cleaning" it — normalizing it to a consistent format."
                                                
                                                — Django documentation

Mas como estamos usando DRF, em 'Form' lê-se 'Serializer'.

https://www.django-rest-framework.org/api-guide/fields/
"""

class ContaSerializer(serializers.ModelSerializer):
    conta_tipo = [('P', 'Poupança'), ('C', 'Corrente')]

    # cliente = serializers.StringRelatedField()
    cliente = ClienteSerializer()
    numero = serializers.CharField(max_length=6, min_length=6, read_only=True)
    agencia = serializers.CharField(max_length=4, min_length=4, required=True)
    dados_sensiveis = serializers.StringRelatedField()
    tipo = serializers.ChoiceField(choices=conta_tipo)

    class Meta:
        model = Conta
        fields = ['cliente', 'agencia', 'numero', 'tipo', 'dados_sensiveis']

    def create(self, validated_data):
        todos_numeros = [x.numero for x in list(Conta.objects.all())]
        while self.numero in todos_numeros:
            self.numero = str(randint(10**5, (10**6)-1))
            validated_data['numero'] = self.numero
        return super().create(validated_data)


class ContaDadosSensiveisSerializer(serializers.ModelSerializer):
    saldo = serializers.DecimalField(max_digits=15, decimal_places=4)

    class Meta:
        model = ContaDadosSensiveis
        fields = ['saldo']


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


