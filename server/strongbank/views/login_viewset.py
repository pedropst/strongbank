from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers.login_serializer import LoginSerializer
from strongbank.serializers.user_serializer import UserSerializer


class LoginViewset(viewsets.ViewSet):
    """
        Classe reponsável por implementar a view do endpoint do login. Para esse 
        endpoint não é necessário autenticação para acessá-lo.
    """
    serializer_calss = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
            Método responsável pela verificação da validação de um login.
        """

        serializer = LoginSerializer(data=request.data, context=request)
        serializer.is_valid(raise_exception=True)
        
        return Response({'status':'Login efetuado com sucesso!'}, status=200)

