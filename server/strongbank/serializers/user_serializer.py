from django.contrib.auth.models import User
from rest_framework import serializers

from strongbank.models.cliente import Cliente

class UserSerializer(serializers.ModelSerializer):
    clientes = serializers.PrimaryKeyRelatedField(many=False, queryset=Cliente.objects.all())
    dono = serializers.ReadOnlyField(source='dono.username')

    class Meta:
        model = User
        fields = ['id', 'username', 'clientes', 'dono']

        