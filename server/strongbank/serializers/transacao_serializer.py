from rest_framework import serializers

from strongbank.models.transacao import Transacao


class TransacaoSerializer(serializers.ModelSerializer):
    """
        Classe responsável pela serialização e deserialização das transações.
        Também possui os métodos validadores para criação de uma transação.
    """

    class Meta:
        model = Transacao
        fields = '__all__'
    
    def validate(self, attrs):
        """
            Validador de uma transação, não aceitando um request que não possua
            tipo, cliente e valor.
        """

        if 'tipo' not in attrs:
            serializers.ValidationError({'Erro':'Transações requerem "tipo".'})
        elif 'cliente' not in attrs:
            serializers.ValidationError({'Erro':'Transações requerem "cliente".'})
        elif 'valor' not in attrs:
            serializers.ValidationError({'Erro':'Transações requerem "valor".'})
        return super().validate(attrs)
        