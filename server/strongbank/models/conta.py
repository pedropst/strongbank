from random import randint
from uuid import uuid4
from django.core.signing import Signer
from django.db import models

from strongbank.entities.acoes_conta import AcoesConta
from strongbank.models.cliente import Cliente


class ContaDadosSensiveis(models.Model):
    """
        Classe responsável por gerar modelo do banco de dados para o registro do
        saldo da conta bancária, ficando separado do restante das informações da
        conta. E possuindo como relação o id da conta, onde uma conta pode possuir,
        um dado sensível (saldo).
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    saldo = models.DecimalField(max_digits=15, decimal_places=2)

    def save(self, *args, **kwargs):
        signer = Signer()
        # self.idconta = signer.sign(self.idconta)
        # saldo = Decimal(self.saldo)
        # self.saldo = signer.sign(self.saldo)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.saldo)


class Conta(AcoesConta, models.Model):
    """
        Classe responsável por gerar modelo do banco de dados para o registro
        das contas, possui os seguintes campos: id, cliente_id, numero, agencia,
        dta_criacao, dados_sensiveis_id e tipo. E possuindo como relação um cliente,
        onde um cliente pode possuir somente uma conta.
    """

    conta_tipo = [("P", "Poupança"), ("C", "Corrente")]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    numero = models.CharField(max_length=6, editable=False)
    agencia = models.CharField(max_length=4)
    dta_criacao = models.DateField(auto_now=True, editable=False)
    dados_sensiveis = models.OneToOneField(
        ContaDadosSensiveis, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=conta_tipo, default=conta_tipo[0][0])

    def save(self, *args, **kwargs):
        todos_numeros = [x.numero for x in list(Conta.objects.all())]
        while self.numero in todos_numeros:
            self.numero = str(randint(10**5, (10**6) - 1))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.cliente.nome
