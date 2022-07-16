from decimal import Decimal
from requests import request
from rest_framework import serializers

from strongbank.models.cartao import Cartao, CartaoDadosSensiveis


class CartaoDadosSensiveisSerializer(serializers.ModelSerializer):
    """
        Classe responsável pela serialização e deserialização dos dados sensíveis,
        do cartão. Não possui métodos validadores, pois, em nada depende do input
        do usuário.
    """
    class Meta:
        model = CartaoDadosSensiveis
        fields = ['id', 'cvv']


class CartaoSerializer(serializers.ModelSerializer):
    """
        Classe responsável pela serialização e deserialização dos cartões. Também
        possui os métodos validadores para criação de um cartão.
    """

    cvv = serializers.ReadOnlyField(source='dados_sensiveis.cvv')
    dia_vencimento = serializers.CharField(max_length=2)
    
    class Meta:
        model = Cartao
        fields = ['id', 'nome', 'dia_vencimento', 'numeracao', 'mes_validade', 'ano_validade', 'cvv', 'limite_total', 'limite_desbloqueado', 'limite_disponivel', 'bloqueado']

    def validate_dia_vencimento(self, dia_vencimento):
        """
            Validador do dia de vencimento de um cartão, permitindo dias somente
            entre 1 e 28 de cada mês.
        """

        if int(dia_vencimento) < 1 or int(dia_vencimento) > 28:
            raise serializers.ValidationError({'ERRO':'Cartão só pode ter vencimento entre os dias 1 e 28.'})
        return dia_vencimento

    def validate_limite_total(self, limite_total):
        """
            Validador do limite total de um cartão, permitindo somente valores
            acima de 0.
        """
        if limite_total <= Decimal(0):
            raise serializers.ValidationError({'ERRO':'Limite tem que ser maior do que 0.'})
        return limite_total


class PagarCreditoSerializer(serializers.Serializer):
    """
        Classe reponsável por implementar as validações de um pagamento feito 
        por crédito. Não tem como base uma classe Modelo, pois, não deseja-se
        fazer nenhum tipo de "armazenamento do pagamento", o responsável por isso
        é o modelo Transacao.
    """

    class Meta:
        fields = ['valor', 'parcelas']

    def validate(self, request):
        """
            Método responsável por verificar que request possui os três campos
            necessários para efetuar o pagamento por crédito: valor, parcelas e
            descrição, contudo, o último campo é opcional.
        """

        if 'valor' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "valor" não informado.'}, code=400)
        elif 'parcelas' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "parcelas" não informado.'}, code=400)
        elif 'descricao' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "descricao" não informado. Contudo, pode vir em branco.'}, code=400)
        return super().validate(request)

    def validate_valor(self, valor):
        """
            Método responsável por verificar que request possui o campo 'valor'
            maior do que 0.
        """

        if valor <= 0:
            raise serializers.ValidationError(('Valor INVÁLIDO.'), code=400)
        return valor

    def validate_parcelas(self, parcelas):
        """
            Método responsável por verificar que request possui o campo 'parcelas'
            maior do que 0 e menor que 12. A restrição em 12 parcelas está relacionado, 
            a lógica utilizada para a geração de parcelas, algo que precisa ser
            melhorado nas próximas atualizações.
        """

        if parcelas <= 0 or parcelas > 12:
            raise serializers.ValidationError(('A quantidade de parcelas precisa ser entre 1 e 12.'), code=400)
        return parcelas


class PagarDebitoSerializer(serializers.Serializer):
    """
        Classe reponsável por implementar as validações de um pagamento feito 
        por débito. Não tem como base uma classe Modelo, pois, não deseja-se
        fazer nenhum tipo de "armazenamento do pagamento", o responsável por isso
        é o modelo Transacao.
    """

    class Meta:
        fields = ['valor', 'descricao']

    def validate(self, request):
        """
            Método responsável por verificar que request possui os três campos
            necessários para efetuar o pagamento por crédito: valor e descrição,
            contudo, o segundo campo é opcional.
        """

        if 'valor' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "valor" não informado.'}, code=400)
        elif 'descricao' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "descricao" não informado.'}, code=400)
        return super().validate(request)

    def validate_valor(self, valor):
        """
            Método responsável por verificar que request possui o campo 'valor'
            maior do que 0.
        """

        if valor <= 0:
            raise serializers.ValidationError(('Valor INVÁLIDO.'), code=400)
        return valor

class AlterarBloqueioSerializer(serializers.Serializer):
    def validate(self, attrs):
        return super().validate(attrs)

class AlterarLimiteSerializer(serializers.Serializer):
    """
        Classe reponsável por implementar as validações da mudança de limite.
    """

    class Meta:
        fields = ['valor', 'descricao']

    def validate(self, request):
        """
            Método responsável por verificar que request possui o campo
            necessário para efetuar a mudança de limite: valor.
        """

        if 'valor' not in (self.context.data.keys()):
            raise serializers.ValidationError({'ERRO':'O "valor" não informado.'}, code=400)
        return super().validate(request)

    def validate_valor(self, valor):
        """
            Método responsável por verificar que request possui o campo 'valor'
            maior do que 0.
        """

        if valor <= 0:
            raise serializers.ValidationError(('Valor INVÁLIDO.'), code=400)
        return valor

