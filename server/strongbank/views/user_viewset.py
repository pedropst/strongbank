from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers.user_serializer import UserSerializer


class UserViewset(viewsets.ViewSet):
    """
        Classe reponsável por implementar a view do endpoint. Para esse endpoint
        não é necessário autenticação para acessá-lo.
    """
    queryset = User.objects.all()
    serializer_calss = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
            Método responsável pela criação de um usuário, e possui a possibilidade
            de criar tanto super usuários (administradores) como usuários comuns.
            A lógica para essa diferenciação está implementada aqui.
        """
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects._create_user(request.data['username'], 
        request.data['email'], request.data['password'])
        user.is_superuser = True if request.data['tipo'] == 'A' else False
        user.save()

        return Response({'status': 'Usuário criado com sucesso!'}, status=201)
        