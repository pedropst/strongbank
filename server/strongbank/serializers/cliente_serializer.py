from rest_framework import serializers

from strongbank.models.cliente import Cliente


"""
"Each field in a Form class is responsible not only for validating data, 
but also for "cleaning" it — normalizing it to a consistent format."
                                                
                                                — Django documentation

Mas como estamos usando DRF, em 'Form' lê-se 'Serializer'.

https://www.django-rest-framework.org/api-guide/fields/
"""

class ClienteSerializer(serializers.ModelSerializer):
    """
        Classe responsável pela serialização e deserialização dos clientes. Também
        possui os métodos validadores para a criação do cliente.
    """

    nome = serializers.CharField(max_length=80)
    endereco = serializers.CharField(max_length=100)
    celular = serializers.CharField(max_length=13)
    documento = serializers.CharField(max_length=14)
    tipo = serializers.CharField(max_length=2)

    class Meta:
        model = Cliente
        fields = ['nome', 'endereco', 'celular', 'documento', 'tipo']
        depth = 1

    def validate(self, data):
        self.validate_tipo_e_documento(data)
        return data

    def validate_nome(self, nome: str) -> None:
        """
            Método responsável por verificar se o nome é composto por nome e 
            sobrenome, ao menos, um de cada.
        """
        if len(nome.split(' ')) < 2:
            raise serializers.ValidationError({'Erro':'Espera-se um nome completo, no mínimo 1 nome e 1 sobrenome.'})
        return nome

    def validate_documento(self, documento: str) -> None:
        """
            Método responsável por verificar se o documento é único na base.
        """
        if self.context.path == '/cliente/' and self.context.method == 'POST':
            cliente = Cliente.objects.filter(documento=documento)
            if cliente:
                raise serializers.ValidationError({'Erro':'Já existe cliente com esse CPF ou CNPJ.'})
        else:
            if not documento.isnumeric():
                serializers.ValidationError({'Erro':'Valor inválido, precisa ser composto somente por números.'})
        return documento

    def validate_tipo_e_documento(self, data) -> None:
        """
            Método responsável por verificar se os campos de CPF e CNPJ foram 
            preenchidos conforme a quantidade de caracteres esperadas.
        """
        if (data.get('tipo') == "PF") and (len(data.get('documento')) != 11):
            raise serializers.ValidationError({'Erro':'Espera-se um CPF válido para um cliente PF.'})
        elif (data.get('tipo') == "PJ") and (len(data.get('documento')) != 14):
            raise serializers.ValidationError({'Erro':'Espera-se um CNPJ válido para um cliente PJ.'})

    def validate_celular(self, celular: str) -> None:
        """
            Método responsável por verificar se a quantidade de dígitos do 
            celular está conforme o modelo: 5567999881520
        """
        if len(celular) != 13:
            raise serializers.ValidationError({'Erro':'Espera-se número de telefone composto só por dígitos, no seguinte modelo: 5567999881520'})
        return celular
