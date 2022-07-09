# from strongbank.models import Cliente, Conta, ContaDadosSensiveis, Documento
from strongbank.models import Cliente, Conta, ContaDadosSensiveis, Transacao
from rest_framework import serializers
from django.contrib.auth.models import User

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
    
class UserSerializer(serializers.ModelSerializer):
    clientes = serializers.PrimaryKeyRelatedField(many=False, queryset=Cliente.objects.all())
    dono = serializers.ReadOnlyField(source='dono.username')

    class Meta:
        model = User
        fields = ['id', 'username', 'clientes', 'dono']

class ClienteSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(max_length=80)
    endereco = serializers.CharField(max_length=100)
    celular = serializers.CharField(max_length=14)
    documento = serializers.CharField(max_length=14)
    tipo = serializers.CharField(max_length=2)

    class Meta:
        model = Cliente
        fields=['nome', 'endereco', 'celular', 'documento', 'tipo']
        depth = 1

    
    def validate(self, data):
        if data.get('cpf') and data.get('cnpj'):
            raise serializers.ValidationError(
                {'DOCUMENTO INVÁLIDO':
                'Campo de CPF e CNPJ preenchidos, escolher somente um.'})
        return data


# class DocumentoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Documento
#         fields = ['id', 'cpf', 'cnpj']

class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields= ['id', 'cliente', 'agencia', 'numero', 'tipo']

class ContaDadosSensiveisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaDadosSensiveis
        fields = ['id', 'saldo']

class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = '__all__'

