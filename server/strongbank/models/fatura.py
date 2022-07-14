from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4
from django.db import models

from strongbank.models.cartao import Cartao


class Fatura(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE)
    mes_ref = models.IntegerField()
    ano_ref = models.IntegerField()
    total = models.DecimalField(max_digits=15, decimal_places=5, default=Decimal(0))
    parcial = models.DecimalField(max_digits=15, decimal_places=5, default=Decimal(0))
    dta_criacao = models.DateField(auto_now=True)

    def criar_vencimento(self):
        self.mes_ref = (datetime.today() + timedelta(days=31)).date().month
        self.ano_ref = (datetime.today() + timedelta(days=31)).date().year

    def __str__(self) -> str:
        return str(self.mes_ref).zfill(2) + str(self.ano_ref)
