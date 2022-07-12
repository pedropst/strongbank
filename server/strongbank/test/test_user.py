import json
from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_cliente_criacao(self):
        User.objects.create(username="bianca", email="bianca@email.com", password="123456")

        user_criado = User.objects.get(username="bianca")

        self.assertEqual(user_criado.username, "bianca")

    def test_cliente_normal_criacao_por_request(self):
        payload = {"username":"bianca", "email":"bianca@email.com", "password":"123456", "tipo": "N"}

        response = self.client.post('/user/', payload, format='json')

        self.assertEqual(response.status_code, 201)

    def test_cliente_admin_criacao_por_request(self):
        payload = {"username":"bianca", "email":"bianca@email.com", "password":"123456", "tipo": "A"}

        self.client.post('/user/', payload, format='json')

        usuario_criado = User.objects.get(username=payload['username'])

        self.assertEqual(usuario_criado.is_superuser, True)
