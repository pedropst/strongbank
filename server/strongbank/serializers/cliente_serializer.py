from rest_framework import serializers

from strongbank.models.cliente import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(max_length=80)
    endereco = serializers.CharField(max_length=100)
    celular = serializers.CharField(max_length=14)
    documento = serializers.CharField(max_length=14)
    tipo = serializers.CharField(max_length=2)

    class Meta:
        model = Cliente
        fields = ['nome', 'endereco', 'celular', 'documento', 'tipo']
        depth = 1

    def validate(self, data):
        if data.get('cpf') and data.get('cnpj'):
            raise serializers.ValidationError(
                {'DOCUMENTO INVÁLIDO':
                'Campo de CPF e CNPJ preenchidos, escolher somente um.'})
        return data