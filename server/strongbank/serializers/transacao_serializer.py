from rest_framework import serializers

from strongbank.models.transacao import Transacao


class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = '__all__'
    
    def validate(self, attrs):
        if 'tipo' not in attrs:
            serializers.ValidationError({'Erro':'Transações requerem "tipo".'})
        elif 'cliente' not in attrs:
            serializers.ValidationError({'Erro':'Transações requerem "cliente".'})
        elif 'valor' not in attrs:
            serializers.ValidationError({'Erro':'Transações requerem "valor".'})
        return super().validate(attrs)

        