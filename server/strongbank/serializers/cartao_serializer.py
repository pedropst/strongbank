from decimal import Decimal
from requests import request
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

    def validate(self, request):
        if 'valor' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "valor" não informado.'}, code=400)
        elif 'parcelas' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "parcelas" não informado.'}, code=400)
        elif 'descricao' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "descricao" não informado.'}, code=400)

        return super().validate(request)

    def validate_valor(self, valor):
        if valor <= 0:
            raise serializers.ValidationError(('Valor INVÁLIDO.'), code=400)
        return valor

    def validate_parcelas(self, parcelas):
        if parcelas <= 0 or parcelas > 12:
            raise serializers.ValidationError(('A quantidade de parcelas precisa ser entre 1 e 12.'), code=400)
        return parcelas

    


class PagarDebitoSerializer(serializers.Serializer):
    class Meta:
        fields = ['valor', 'descricao']

    def validate(self, request):
        if 'valor' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "valor" não informado.'}, code=400)
        elif 'descricao' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "descricao" não informado.'}, code=400)

        return super().validate(request)

    def validate_valor(self, valor):
        if valor <= 0:
            raise serializers.ValidationError(('Valor INVÁLIDO.'), code=400)
        return valor

    def validate_valor(self, descricao):
        if not descricao:
            raise serializers.ValidationError(('Descrição INVÁLIDA.'), code=400)
        return descricao
