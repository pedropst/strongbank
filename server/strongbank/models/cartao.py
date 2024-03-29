from datetime import datetime
from decimal import Decimal
from typing import Any
from django.db import models
from uuid import uuid4

from strongbank.entities.acoes_cartao import AcoesCartao
from strongbank.models.conta import Conta


class CartaoDadosSensiveis(models.Model):
    """
        Classe responsável por gerar modelo do banco de dados para o registro do
        cvv do cartão, ficando separado do restante das informações do cartão. E 
        possuindo como relação o id do cartão.
    """
    cvv = models.CharField(max_length=3, editable=False)

    # def save(self, *args, **kwargs):
    #     self.cvv = encrypt(self.cvv, os.getenv('SECRET_KET'))
    #     super().save(*args, **kwargs)


class Cartao(AcoesCartao, models.Model):
    """
        Classe responsável por gerar modelo do banco de dados para o registro
        dos cartões, possui os seguintes campos: id, conta_id, dia_vencimento,
        nome, mes_validade, ano_validade, bloqueado, dta_criacao, limite_total,
        limite_disponivel, limite_desbloqueado, bandeira e dados_sensiveis_id.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    conta = models.OneToOneField(Conta, on_delete=models.CASCADE)
    dia_vencimento = models.IntegerField(
        choices=[(x + 1, f"Dia {x+1}") for x in range(28)])
    nome = models.CharField(max_length=30, editable=False, default="")
    mes_validade = models.CharField(
        max_length=2, editable=False, default=str(datetime.today().month))
    ano_validade = models.CharField(
        max_length=4, editable=False, default=str(datetime.today().year + 8))

    bloqueado = models.BooleanField(editable=False, default=True)
    dta_criacao = models.DateField(auto_now=True)
    numeracao = models.CharField(max_length=16, editable=False)
    dados_sensiveis = models.OneToOneField(
        CartaoDadosSensiveis, on_delete=models.CASCADE)
    limite_total = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal(0))
    limite_disponivel = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal(0))
    limite_desbloqueado = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal(0))
    bandeira = models.CharField(max_length=20)

    def __str__(self) -> Any:
        return self.nome
