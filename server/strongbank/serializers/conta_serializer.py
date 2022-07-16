from decimal import Decimal
from random import randint
from rest_framework import serializers

from strongbank.models.cliente import Cliente
from strongbank.models.conta import Conta, ContaDadosSensiveis
from strongbank.models.transacao import Transacao
from strongbank.serializers.cliente_serializer import ClienteSerializer
from strongbank.serializers.transacao_serializer import TransacaoSerializer


class ContaSerializer(serializers.ModelSerializer):
    """
        Classe responsável pela serialização e deserialização das contas. Também
        possui os métodos validadores para criação de uma conta.
    """

    conta_tipo = [('P', 'Poupança'), ('C', 'Corrente')]

    cliente = ClienteSerializer()
    numero = serializers.CharField(max_length=6, min_length=6, read_only=True)
    agencia = serializers.CharField(max_length=4, min_length=4, required=True)
    dados_sensiveis = serializers.StringRelatedField()
    tipo = serializers.ChoiceField(choices=conta_tipo)

    class Meta:
        model = Conta
        fields = ['cliente', 'agencia', 'numero', 'tipo', 'dados_sensiveis']

    def create(self, validated_data):
        """
            Método responsável pela criação de uma conta, ele contém a lógica para
            a geração do número da conta, que é aleatório e único (em relação a 
            base toda, apesar de não ser o primary key).
        """

        todos_numeros = [x.numero for x in list(Conta.objects.all())]
        while self.numero in todos_numeros:
            self.numero = str(randint(10**5, (10**6)-1))
            validated_data['numero'] = self.numero
        return super().create(validated_data)

    def validate_agencia(self, agencia):
        """
            Validador da agência de uma conta, permitindo somente número de agência
            composto por 4 digítos.
        """

        if len(agencia) != 4:
            raise serializers.ValidationError(("Número de 'agência' INVÁLIDO."), code=400)
        return agencia


class ContaDadosSensiveisSerializer(serializers.ModelSerializer):
    """
        Classe responsável pela serialização e deserialização dos dados sensíveis,
        da conta. Não possui métodos validadores, pois, em nada depende do input
        do usuário.
    """

    saldo = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        model = ContaDadosSensiveis
        fields = ['saldo']

    def validate(self, attrs):
        """
            Validador do saldo inicial de uma conta, não permitindo a criação de
            contas com saldo inicial negativo.
        """

        if attrs.get('saldo') < 0:
            raise serializers.ValidationError(('Saldo INVÁLIDO.'), code=400)
        return super().validate(attrs)


class TransferirSerializer(serializers.Serializer):
    """
        Classe reponsável por implementar as validações de uma transferência. 
        Não tem como base uma classe Modelo, pois, não deseja-se fazer nenhum 
        tipo de "armazenamento do pagamento", o responsável por isso é o modelo
        Transacao.
    """

    valor = serializers.DecimalField(max_digits=15, decimal_places=2)
    senha = serializers.CharField(max_length=300)
    
    class Meta:
        fields = ['doc_remetente', 'valor', 'doc_destinatario', 'senha']

    def validate_valor(self, valor):
        """
            Método responsável por verificar que request possui o campo 'valor'
            maior do que 0.
        """

        if valor <= 0:
            raise serializers.ValidationError(('Valor INVÁLIDO.'), code=400)
        return valor

    def validate_senha(self, senha: str) -> None:
        """
            Método responsável por verificar que request possui o campo 'senha'
            válido, conforme a senha do usuário.
        """

        if not self.context.user.check_password(senha):
            raise serializers.ValidationError(('Senha INVÁLIDA.'), code=400)
        return senha


class SacarSerializer(serializers.Serializer):
    """
        Classe reponsável por implementar as validações de um saque. Não tem como 
        base uma classe Modelo, pois, não deseja-se fazer nenhum tipo de 
        "armazenamento da operação", o responsável por isso é o modelo Transacao.
    """

    valor = serializers.DecimalField(max_digits=15, decimal_places=2)
    senha = serializers.CharField(max_length=300)
    
    class Meta:
        fields = ['valor', 'senha']

    def validate_valor(self, valor):
        """
            Método responsável por verificar que request possui o campo 'valor'
            maior do que 0.
        """

        if valor <= 0:
            raise serializers.ValidationError({'Erro':'Valor inválido, precisa ser maior do que 0.'})
        elif not str(valor).split('.')[0].isnumeric() and str(valor).split('.')[1].isnumeric():
            raise serializers.ValidationError({'Erro':'Valor inválido, precisa ser composto somente por números.'})
        return valor

    def validate_senha(self, senha: str) -> None:
        """
            Método responsável por verificar que request possui o campo 'senha'
            válido, conforme a senha do usuário.
        """

        if not self.context.user.check_password(senha):
            raise serializers.ValidationError({'Erro':'Senha inválida, não corresponde a senha do login.'}, code=400)
        return senha


class DepositarSerializer(serializers.Serializer):
    """
        Classe reponsável por implementar as validações de um depósito. Não tem 
        como base uma classe Modelo, pois, não deseja-se fazer nenhum tipo de 
        "armazenamento da operação", o responsável por isso é o modelo Transacao.
    """

    valor = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        fields = ['valor']

    def validate_valor(self, valor):
        """
            Método responsável por verificar que request possui o campo 'valor'
            maior do que 0.
        """

        if valor <= 0:
            raise serializers.ValidationError({'Erro':'Valor inválido, precisa ser maior do que 0.'})
        elif not str(valor).split('.')[0].isnumeric() and str(valor).split('.')[1].isnumeric():
            raise serializers.ValidationError({'Erro':'Valor inválido, precisa ser composto somente por números.'})
        return valor

class SaldoSerializer(serializers.Serializer):
    """
        Classe reponsável por implementar as validações de um saldo. Não tem 
        como base uma classe Modelo, pois, não deseja-se fazer nenhum tipo de 
        "armazenamento da operação", sendo um endpoint só de GET.
    """

    class Meta:
        fields = ['documento']
    