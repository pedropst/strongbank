from datetime import datetime
from decimal import Decimal
from django.db import models

from uuid import uuid4

from strongbank.models.cliente import Cliente


class Transacao(models.Model):
    """
        Classe responsável por gerar modelo do banco de dados para o registro
        das transações, possui os seguintes campos: id, cliente_id, tipo, valor,
        dta_criacao e descrição. E possuindo como relação um cliente, onde um 
        cliente pode possuir diversas transações.
    """

    acoes_tipo = [
        ("S", "Saque"),
        ("D", "Deposito"),
        ("TE", "Transferência Efetuada"),
        ("TR", "Transferência Recebida"),
        ("C", "Cartão"),
        ("PC", "Pagamento por Cartão"),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, unique=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=acoes_tipo, default=acoes_tipo[0][0])
    dta_criacao = models.DateTimeField(auto_now=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    descricao = models.CharField(max_length=30, blank=True)

    def save(self, *args, **kwargs):
        if self.tipo in ["S", "T", "C"]:
            self.valor = Decimal(self.valor) * Decimal(-1)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.tipo} -> {self.valor}"
