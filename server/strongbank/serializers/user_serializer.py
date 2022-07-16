from django.contrib.auth.models import User
from rest_framework import serializers

from strongbank.models.cliente import Cliente

class UserSerializer(serializers.ModelSerializer):
    # clientes = serializers.PrimaryKeyRelatedField(many=False, queryset=Cliente.objects.all())
    dono = serializers.ReadOnlyField(source='dono.username')

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'dono']

    def validate_username(self, username):
        if len(username) < 6:
            raise serializers.ValidationError({'ERRO':'Username precisa ter ao menos 6 caracteres.'})
        
        return username

    def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError({'ERRO':'Password precisa ter ao menos 6 caracteres.'})
        
        return password

        