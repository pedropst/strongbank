from django.core.signing import Signer
from django.db import models
from random import randint
from uuid import uuid4

from strongbank.entities.conta import AcoesConta
from strongbank.models.cliente import Cliente


class ContaDadosSensiveis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    saldo = models.DecimalField(max_digits=15, decimal_places=5)
    # saldo = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        signer = Signer()
        # self.idconta = signer.sign(self.idconta)
        # saldo = Decimal(self.saldo)
        # self.saldo = signer.sign(self.saldo)
        super().save(*args, **kwargs)


class Conta(AcoesConta, models.Model):
    conta_tipo = [('P', 'Poupança'), ('C', 'Corrente')]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    numero = models.CharField(max_length=6, editable=False)
    agencia = models.CharField(max_length=4)
    dta_criacao = models.DateField(auto_now=True)
    dados_sensiveis = models.OneToOneField(ContaDadosSensiveis, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=conta_tipo, default=conta_tipo[0][0])
    # dados = ContaDadosSensiveis()
    # dados.saldo += 50

    def save(self, *args, **kwargs):
        todos_numeros = [x.numero for x in list(Conta.objects.all())]
        while self.numero in todos_numeros:
            self.numero = str(randint(10**5, (10**6)-1))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.cliente.nome

