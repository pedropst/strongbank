from decimal import Decimal
from rest_framework import serializers

from strongbank.models.cartao import Cartao, CartaoDadosSensiveis


class CartaoDadosSensiveisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaoDadosSensiveis
        fields = ['id', 'cvv']


class CartaoSerializer(serializers.ModelSerializer):
    cvv = serializers.ReadOnlyField(source='dados_sensiveis.cvv')
    dia_vencimento = serializers.CharField(max_length=2)
    
    class Meta:
        model = Cartao
        fields = ['nome', 'dia_vencimento', 'numeracao', 'mes_validade', 'ano_validade', 'cvv', 'limite_total', 'limite_desbloqueado', 'limite_disponivel', 'bloqueado']

    def validate_dia_vencimento(self, dia_vencimento):
        if int(dia_vencimento) < 1 or int(dia_vencimento) > 28:
            raise serializers.ValidationError({'ERRO':'Cartão só pode ter vencimento entre os dias 1 e 28.'})
        return dia_vencimento

    def validate_limite_total(self, limite_total):
        if limite_total <= Decimal(0):
            raise serializers.ValidationError({'ERRO':'Limite tem que ser maior do que 0.'})
        return limite_total

class PagarCreditoSerializer(serializers.Serializer):
    class Meta:
        fields = ['valor', 'parcelas']


class PagarDebitoSerializer(serializers.Serializer):
    class Meta:
        fields = ['valor']

