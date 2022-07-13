from decimal import Decimal
from random import randint
from rest_framework import serializers

from strongbank.models.cliente import Cliente
from strongbank.models.conta import Conta, ContaDadosSensiveis
from strongbank.models.transacao import Transacao
from strongbank.serializers.cliente_serializer import ClienteSerializer
from strongbank.serializers.transacao_serializer import TransacaoSerializer


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
    valor = serializers.DecimalField(max_digits=15, decimal_places=4)
    senha = serializers.CharField(max_length=300)
    
    class Meta:
        fields = ['doc_remetente', 'valor', 'doc_destinatario', 'senha']

    def validate_valor(self, valor):
        if valor <= 0:
            raise serializers.ValidationError(('Valor INVÁLIDO.'), code=400)
        return valor

    def validate_senha(self, senha: str) -> None:
        if not self.context.user.check_password(senha):
            raise serializers.ValidationError(('Senha INVÁLIDA.'), code=400)
        return senha


class SacarSerializer(serializers.Serializer):
    valor = serializers.DecimalField(max_digits=15, decimal_places=4)
    senha = serializers.CharField(max_length=300)
    
    class Meta:
        fields = ['valor', 'senha']

    def validate_valor(self, valor):
        if valor <= 0:
            raise serializers.ValidationError(('Valor INVÁLIDO.'), code=400)
        return valor

    def validate_senha(self, senha: str) -> None:
        if not self.context.user.check_password(senha):
            raise serializers.ValidationError(('Senha INVÁLIDA.'), code=400)
        return senha


class DepositarSerializer(serializers.Serializer):
    class Meta:
        fields = ['documento', 'valor']


class SaldoSerializer(serializers.Serializer):
    class Meta:
        fields = ['documento']
    
