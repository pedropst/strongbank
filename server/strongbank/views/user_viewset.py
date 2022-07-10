from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from strongbank.permissions import IsOwnerOrReadOnly, IsUpdateProfile
from strongbank.serializers.user_serializer import UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        user = User.objects._create_user(request.data['username'], request.data['email'], request.data['senha'])
        user.is_superuser = True if request.data['tipo'] == 'A' else False
        user.save()
        return Response({'status': 'Usuário criado com sucesso!'}, status=201)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

