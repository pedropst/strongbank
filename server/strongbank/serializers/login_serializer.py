from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
        Classe reponsável por implementar as validações da efetuação de um login. 
        Não tem como base uma classe Modelo, pois, não deseja-se fazer nenhum 
        tipo de "armazenamento do login".
    """

    username = serializers.CharField(max_length=20)
    password = serializers.CharField(min_length=6, max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, request):
        """
            Validador do login de uma conta, não permitindo o login com usuário
            ou senha inválida.
        """
        user = User.objects.filter(username=request.get('username')).all()
        if user:
            if not user[0].check_password(request.get('password')):
                raise serializers.ValidationError({'password':'Senha INVÁLIDA.'}, code=400)
            return super().validate(request)
        else:
                raise serializers.ValidationError({'username':'Usuário INVÁLIDO.'}, code=400)
