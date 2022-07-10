from rest_framework import serializers

from strongbank.models.transacao import Transacao


class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = '__all__'

        