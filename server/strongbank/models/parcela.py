from decimal import Decimal
from django.db import models
from uuid import uuid4

from strongbank.models.fatura import Fatura


class Parcela(models.Model):
    """
        Classe responsável por gerar modelo do banco de dados para o registro
        das parcelas, possui os seguintes campos: id, fatura_id, descricao, 
        valor, dta_criacao. A relação existente é com as faturas, onde uma fatura
        pode possuir diversas parcelas.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=20, editable=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0))
    dta_criacao = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.descricao
